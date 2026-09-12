"""Turn scenario scripts into two-voice audio with ElevenLabs.

    PYTHONPATH=src python -m complaintguard.audio.tts --dry-run
    PYTHONPATH=src python -m complaintguard.audio.tts demo-001 demo-003

This is why the corpus is honest: we wrote the scripts, so we know exactly what
was promised and what went unresolved. Voicing them gives us real audio to
demonstrate the full pipeline with no privacy risk at all — and it makes
ElevenLabs load-bearing rather than decorative, which is what the special track
asks for.

Output lands in data/audio/<case_id>/<NN>-<speaker>.mp3, one file per utterance,
plus a manifest. Per-utterance rather than per-call because a single line can be
re-recorded without paying for the whole conversation again.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

import httpx

from .. import scenarios

API = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
AUDIO_DIR = Path(__file__).resolve().parents[3] / "data" / "audio"

# Two distinct voices so diarisation has something real to separate. These are
# ElevenLabs' stock voices; swap for any others from the voice library.
VOICES: Dict[str, str] = {
    "customer": os.environ.get("EL_VOICE_CUSTOMER", "21m00Tcm4TlvDq8ikWAM"),
    "agent": os.environ.get("EL_VOICE_AGENT", "AZnzlk1XvdvUeBnXmlld"),
}
MODEL = os.environ.get("EL_TTS_MODEL", "eleven_multilingual_v2")


def _key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise SystemExit(
            "ELEVENLABS_API_KEY is not set.\n"
            "Claim your month of Creator first — see docs/resources.md — then put the\n"
            "key in .env (gitignored). Use --dry-run to check the plan without a key."
        )
    return key


def synth(text: str, speaker: str, out: Path, key: str) -> int:
    """Generate one line. Returns bytes written."""
    resp = httpx.post(
        API.format(voice_id=VOICES[speaker]),
        headers={"xi-api-key": key, "content-type": "application/json"},
        json={
            "text": text,
            "model_id": MODEL,
            "voice_settings": {"stability": 0.45, "similarity_boost": 0.75},
        },
        timeout=120,
    )
    resp.raise_for_status()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    return len(resp.content)


def plan(case_ids: Optional[List[str]] = None) -> List[dict]:
    """What would be generated, and what is already on disk."""
    index = scenarios.scenario_index()
    chosen = case_ids or list(index)
    jobs: List[dict] = []
    for cid in chosen:
        if cid not in index:
            print("  ! no such scenario: {}".format(cid), file=sys.stderr)
            continue
        case = scenarios.load_case(index[cid])
        for contact in case.contacts:
            if not contact.transcript:
                continue
            for i, u in enumerate(contact.transcript.utterances):
                out = AUDIO_DIR / cid / "{}-{:02d}-{}.mp3".format(contact.seq, i, u.speaker.value)
                jobs.append(
                    {
                        "case": cid,
                        "contact": contact.seq,
                        "index": i,
                        "speaker": u.speaker.value,
                        "chars": len(u.text),
                        "text": u.text,
                        "out": out,
                        "exists": out.exists(),
                    }
                )
    return jobs


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cases", nargs="*", help="scenario ids; default is all")
    ap.add_argument("--dry-run", action="store_true", help="show the cost, call nothing")
    ap.add_argument("--force", action="store_true", help="regenerate files that already exist")
    args = ap.parse_args(argv)

    jobs = plan(args.cases or None)
    todo = [j for j in jobs if args.force or not j["exists"]]
    chars = sum(j["chars"] for j in todo)

    print("{} lines total, {} already generated, {} to do".format(
        len(jobs), len(jobs) - len(todo), len(todo)))
    # Text-to-speech bills at roughly one credit per character; the Creator tier
    # is 121,000 a month and speech-to-text draws on the same pool.
    print("~{:,} characters ≈ ~{:,} credits of a 121,000/month allowance".format(chars, chars))

    if args.dry_run:
        for j in todo[:8]:
            print("  {} c{} #{:02d} {:<9} {:>4} chars".format(
                j["case"], j["contact"], j["index"], j["speaker"], j["chars"]))
        if len(todo) > 8:
            print("  ... and {} more".format(len(todo) - 8))
        return 0

    if not todo:
        print("nothing to do")
        return 0

    key = _key()
    written = 0
    for j in todo:
        size = synth(j["text"], j["speaker"], j["out"], key)
        written += size
        print("  {} -> {:,} bytes".format(j["out"].name, size))

    manifest = AUDIO_DIR / "manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(
        [{k: (str(v) if isinstance(v, Path) else v) for k, v in j.items() if k != "text"}
         for j in jobs], indent=2), encoding="utf-8")
    print("wrote {:,} bytes across {} files".format(written, len(todo)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
