// Execute the live room's script against a stub DOM and report what it touches.
//
// `node --check` proves the file parses. It does not prove the code runs, and the
// bug that made this necessary was exactly that gap: a function was deleted by a
// careless slice edit, the file still parsed, and the page threw ReferenceError
// the first time anyone clicked the microphone. A judge would have found it.
//
//   node tools/check_room_js.js <file.js>
//
// Exits non-zero on ReferenceError or TypeError. This is a smoke test, not a
// browser: it proves every identifier the module body and its handlers reach is
// defined, which is the class of mistake that keeps happening here.

const fs = require('fs');
const vm = require('vm');

const src = fs.readFileSync(process.argv[2], 'utf8');
const listeners = {};
const problems = [];

function element(id) {
  const el = {
    id, hidden: false, disabled: false, textContent: '', innerHTML: '', value: '',
    title: '', src: '', dataset: {}, children: [], style: {},
    classList: { add() {}, remove() {}, contains: () => false, toggle() {} },
    addEventListener(type, fn) { (listeners[id + ':' + type] ||= []).push(fn); },
    removeEventListener() {}, appendChild() {}, remove() {}, focus() {}, click() {},
    querySelector: () => element('child'), querySelectorAll: () => [],
    closest: () => null, scrollIntoView() {}, dispatchEvent() {}, insertBefore() {},
    setAttribute() {}, getAttribute: () => null, hasAttribute: () => false,
  };
  return el;
}

const doc = {
  getElementById: (id) => element(id),
  querySelector: () => element('q'),
  querySelectorAll: () => [],
  createElement: () => element('new'),
  addEventListener(type, fn) { (listeners['document:' + type] ||= []).push(fn); },
  body: element('body'),
};

const sandbox = {
  document: doc,
  console: { log() {}, warn() {}, error() {} },
  setTimeout: () => 0, clearTimeout() {}, setInterval: () => 0, clearInterval() {},
  // A complete, plausible response. An earlier version returned {ok:true} with
  // no session id, so every handler bailed at `if (!sid) return` and the checker
  // walked none of the code it exists to check.
  fetch: () => Promise.resolve({
    json: () => Promise.resolve({
      ok: true, session: 'test-session', turns_left: 7, calls_left_today: 20,
      customer_text: 'hello', agent_text: 'hi there', audio: '/live/say/abc',
      turn: 1, ready: true, score: 40, band: 'medium', signals: [], escalate: false,
      intervention: null, telemetry: {},
    }),
  }),
  FormData: class { append() {} },
  Blob: class { constructor() { this.size = 0; this.type = 'audio/webm'; } },
  Audio: class { play() { return Promise.resolve(); } pause() {} },
  MediaRecorder: class {
    constructor() {
      this.state = 'inactive';
      this.mimeType = 'audio/webm';
      (sandbox.__recorders ||= []).push(this);
    }
    start() { this.state = 'recording'; }
    stop() { this.state = 'inactive'; if (this.onstop) this.onstop(); }
  },
  navigator: {
    mediaDevices: {
      // Succeeds. The first version of this checker rejected, and so never
      // reached the code that assigns the recorder's handlers — which is exactly
      // where the bug it was written to catch lived. A checker has to walk the
      // path a person walks.
      getUserMedia: () => Promise.resolve({ getTracks: () => [{ stop() {} }] }),
      enumerateDevices: () => Promise.resolve([{ kind: 'audioinput', label: '' }]),
    },
    userAgent: 'node',
  },
  location: { hash: '', pathname: '/live', reload() {} },
  isSecureContext: true,
  Date, Promise, Math, JSON, Array, Object, String, Number, Error,
};
sandbox.window = sandbox;
sandbox.MediaRecorder.isTypeSupported = () => true;

try {
  vm.runInNewContext(src, sandbox, { timeout: 5000 });
} catch (e) {
  problems.push('module body: ' + e.name + ': ' + e.message);
}

// Fire every handler the script registered, once per control it dispatches on,
// and let the microtask queue drain — most of this code lives in promise
// callbacks and a synchronous try/catch would never see it.
process.on('unhandledRejection', (e) => {
  if (e instanceof ReferenceError || e instanceof TypeError) {
    problems.push('async: ' + e.name + ': ' + e.message);
  }
});

function fire(selector) {
  const ev = {
    preventDefault() {}, stopPropagation() {}, key: 'Enter',
    target: { closest: (sel) => (sel === selector ? element('x') : null) },
  };
  for (const [key, fns] of Object.entries(listeners)) {
    for (const fn of fns) {
      try { fn(ev); } catch (e) {
        if (e instanceof ReferenceError || e instanceof TypeError) {
          problems.push(key + ' [' + selector + ']: ' + e.name + ': ' + e.message);
        }
      }
    }
  }
}

async function settle() {
  for (let i = 0; i < 40; i++) await Promise.resolve();
  await new Promise((r) => setImmediate(r));
  for (let i = 0; i < 40; i++) await Promise.resolve();
}

// Order matters: start the call first so `sid` is set, then everything that
// refuses to run without one.
async function walk() {
  fire('#begin');
  await settle();
  for (const sel of ['.opener', '#send', '#mic', '#micdiag']) {
    fire(sel);
    await settle();
  }
  // A second #mic click is the stop-and-send path, which is where the recorder's
  // handlers get called.
  fire('#mic');
  await settle();
  if (sandbox.__recorders) {
    for (const r of sandbox.__recorders) {
      try { if (r.onstop) r.onstop(); } catch (e) {
        if (e instanceof ReferenceError || e instanceof TypeError) {
          problems.push('recorder.onstop: ' + e.name + ': ' + e.message);
        }
      }
      try { if (r.ondataavailable) r.ondataavailable({ data: { size: 10 } }); } catch (e) {
        if (e instanceof ReferenceError || e instanceof TypeError) {
          problems.push('recorder.ondataavailable: ' + e.name + ': ' + e.message);
        }
      }
    }
  }
  await settle();
}

walk().then(() => {
if (problems.length) {
  console.error('FAIL');
  problems.forEach((p) => console.error('  ' + p));
  process.exit(1);
}
console.log('OK — module body and ' + Object.keys(listeners).length + ' handler(s) ran clean');
});
