#!/usr/bin/env python3
"""Find the dead time in a screen recording: silent AND visually still.

    python tools/tighten_video.py demo.mp4                 # report only
    python tools/tighten_video.py demo.mp4 --write out.mp4 # cut it

Either signal on its own gets it wrong. Cutting every silence throws away the
moments that carry the demo without a word over them — the alarm appearing, the
score climbing. Cutting every still frame throws away the deliberate pause on a
finding while the narrator explains it. **Dead time is where both are true at
once**, and that is the only thing this removes by default.

A note on the rubric, because it cuts the other way: the organisers exclude
"narration over static screens". Talking over a frozen page is not dead time by
this measure — it is kept — but it is the thing the rule names, so the report
lists those stretches separately as something to fix by moving the mouse, not by
cutting.

`--speed` additionally speeds up stretches that are still but NOT silent, and the
waits that are moving but silent, rather than deleting them. A viewer needs to
see the agent answering; they do not need to wait for it in real time.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
from typing import List, Tuple

Span = Tuple[float, float]

# Two-tenths of a second of air either side of a cut, so a clipped word does not
# lose its first or last consonant.
PAD = 0.20
# Anything shorter than this is not worth a cut: the join costs more attention
# than the time it saves.
MIN_CUT = 0.45


def run(args: List[str]) -> str:
    proc = subprocess.run(args, capture_output=True, text=True)
    return proc.stderr + proc.stdout


def duration(path: str) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", path]).strip().splitlines()
    return float(out[-1])


def silences(path: str, noise: str, min_d: float) -> List[Span]:
    log = run(["ffmpeg", "-hide_banner", "-i", path, "-af",
               "silencedetect=noise={}:d={}".format(noise, min_d), "-f", "null", "-"])
    spans, start = [], None
    for line in log.splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", line)
        if m:
            start = max(0.0, float(m.group(1)))
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m and start is not None:
            spans.append((start, float(m.group(1))))
            start = None
    return spans


def freezes(path: str, noise: str, min_d: float) -> List[Span]:
    log = run(["ffmpeg", "-hide_banner", "-i", path, "-vf",
               "freezedetect=n={}:d={}".format(noise, min_d), "-map", "0:v",
               "-f", "null", "-"])
    spans, start = [], None
    for line in log.splitlines():
        m = re.search(r"freeze_start:\s*(-?[\d.]+)", line)
        if m:
            start = max(0.0, float(m.group(1)))
        m = re.search(r"freeze_end:\s*([\d.]+)", line)
        if m and start is not None:
            spans.append((start, float(m.group(1))))
            start = None
    return spans


def intersect(a: List[Span], b: List[Span]) -> List[Span]:
    out = []
    for s1, e1 in a:
        for s2, e2 in b:
            s, e = max(s1, s2), min(e1, e2)
            if e - s > 0:
                out.append((s, e))
    return merge(out)


def subtract(whole: List[Span], parts: List[Span]) -> List[Span]:
    """What is in `whole` but not in `parts`."""
    out = []
    for s, e in whole:
        cuts = sorted((max(s, cs), min(e, ce)) for cs, ce in parts
                      if min(e, ce) > max(s, cs))
        cursor = s
        for cs, ce in cuts:
            if cs > cursor:
                out.append((cursor, cs))
            cursor = max(cursor, ce)
        if cursor < e:
            out.append((cursor, e))
    return merge(out)


def merge(spans: List[Span]) -> List[Span]:
    if not spans:
        return []
    spans = sorted(spans)
    out = [list(spans[0])]
    for s, e in spans[1:]:
        if s <= out[-1][1] + 0.01:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [(s, e) for s, e in out]


def shrink(spans: List[Span], pad: float, floor: float) -> List[Span]:
    out = []
    for s, e in spans:
        s2, e2 = s + pad, e - pad
        if e2 - s2 >= floor:
            out.append((s2, e2))
    return out


def parse_span(text: str) -> Span:
    """'1:05-1:25' or '65-85' -> (65.0, 85.0)."""
    def one(tok: str) -> float:
        tok = tok.strip()
        if ":" in tok:
            m, sec = tok.split(":", 1)
            return int(m) * 60 + float(sec)
        return float(tok)
    lo, hi = text.split("-", 1)
    return (one(lo), one(hi))


def clock(t: float) -> str:
    return "%d:%05.2f" % (t // 60, t % 60)


def keeps(total: float, cuts: List[Span]) -> List[Span]:
    return subtract([(0.0, total)], cuts)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--write", metavar="OUT", help="write the tightened video")
    ap.add_argument("--target", type=float, default=270.0,
                    help="seconds you are aiming for (default 270 = 4:30)")
    ap.add_argument("--noise", default="-32dB", help="silence threshold")
    ap.add_argument("--min-silence", type=float, default=0.5)
    ap.add_argument("--freeze-noise", default="-55dB", help="freeze sensitivity")
    ap.add_argument("--min-freeze", type=float, default=0.5)
    ap.add_argument("--keep", action="append", default=[], metavar="MM:SS-MM:SS",
                    help="protect a stretch from cutting entirely, e.g. --keep 1:05-1:25. "
                         "Repeatable. Use it where a pause is part of what you want seen.")
    ap.add_argument("--json", metavar="FILE", help="write every cut point as JSON")
    ap.add_argument("--speed", type=float, default=0.0,
                    help="also speed up still-but-talking and moving-but-silent "
                         "stretches by this factor, e.g. 2.0")
    a = ap.parse_args(argv)

    total = duration(a.video)
    print("source          %s  (%.1fs)" % (clock(total), total))
    print("target          %s\n" % clock(a.target))

    print("scanning for silence…", file=sys.stderr)
    sil = merge(silences(a.video, a.noise, a.min_silence))
    print("scanning for still frames…", file=sys.stderr)
    frz = merge(freezes(a.video, a.freeze_noise, a.min_freeze))

    dead = shrink(intersect(sil, frz), PAD, MIN_CUT)

    protected = [parse_span(k) for k in a.keep]
    if protected:
        before = sum(e - s for s, e in dead)
        dead = subtract(dead, protected)
        dead = [(s, e) for s, e in dead if e - s >= MIN_CUT]
        held = before - sum(e - s for s, e in dead)
        print("protected       %d stretch(es), holding %.1fs that would have been cut\n"
              % (len(protected), held))
    dead_s = sum(e - s for s, e in dead)
    sil_s = sum(e - s for s, e in sil)
    frz_s = sum(e - s for s, e in frz)

    # Talking over a frozen screen: kept, but it is the thing the rules name.
    narrated_still = shrink(subtract(frz, sil), PAD, 1.5)
    narr_s = sum(e - s for s, e in narrated_still)

    print("silent              %6.1fs  (%4.1f%%)" % (sil_s, 100 * sil_s / total))
    print("visually still      %6.1fs  (%4.1f%%)" % (frz_s, 100 * frz_s / total))
    print("BOTH — dead time    %6.1fs  (%4.1f%%)   <- safe to cut, %d cuts"
          % (dead_s, 100 * dead_s / total, len(dead)))

    after = total - dead_s
    print("\nafter cutting dead time: %s" % clock(after))
    if after <= 300:
        print("  ✅ under the 5:00 limit" + ("" if after >= 180 else "  ⚠️ but under 3:00!"))
    else:
        print("  ❌ still %s over 5:00 — needs %.0fs more"
              % (clock(after - 300), after - 300))
    if after > a.target:
        print("  %.0fs above your %s target" % (after - a.target, clock(a.target)))

    if narrated_still:
        print("\n⚠️ %.0fs of narration over a still screen, in %d stretches."
              % (narr_s, len(narrated_still)))
        print("   The organisers exclude \"narration over static screens\". Not dead")
        print("   time and not cut here — fix by scrolling or clicking while you talk,")
        print("   or speed these up. Longest:")
        for s, e in sorted(narrated_still, key=lambda x: x[1] - x[0], reverse=True)[:5]:
            print("     %s – %s  (%.1fs)" % (clock(s), clock(e), e - s))

    if dead:
        print("\ncuts (%d):" % len(dead))
        for s, e in dead[:30]:
            print("  %s – %s   %.2fs" % (clock(s), clock(e), e - s))
        if len(dead) > 30:
            print("  … and %d more" % (len(dead) - 30))

    if a.json:
        import json
        pathlib.Path(a.json).write_text(json.dumps(
            {"source": a.video, "duration": total, "speed": a.speed or 1.0,
             "cuts": [{"start": s, "end": e} for s, e in dead],
             "keeps": [{"start": s, "end": e} for s, e in keeps(total, dead)]}, indent=2))
        print("\nwrote %s" % a.json)

    if not a.write:
        print("\nrun again with --write out.mp4 to apply")
        return 0

    segs = keeps(total, dead)
    if not segs:
        print("nothing left to keep", file=sys.stderr)
        return 1

    # One filter_complex pass: trim each kept segment, then concat. Re-encodes,
    # which is the point — a keyframe-aligned copy would drift out of sync.
    parts, v_in, a_in = [], [], []
    for i, (s, e) in enumerate(segs):
        parts.append("[0:v]trim=start=%.3f:end=%.3f,setpts=PTS-STARTPTS[v%d]" % (s, e, i))
        parts.append("[0:a]atrim=start=%.3f:end=%.3f,asetpts=PTS-STARTPTS[a%d]" % (s, e, i))
        v_in.append("[v%d]" % i)
        a_in.append("[a%d]" % i)
    chain = ";".join(parts) + ";" + "".join(
        v + b for v, b in zip(v_in, a_in)) + "concat=n=%d:v=1:a=1[v][a]" % len(segs)

    if a.speed and a.speed > 1.0:
        chain += ";[v]setpts=PTS/%.3f[vf];[a]atempo=%.3f[af]" % (a.speed, min(a.speed, 2.0))
        vmap, amap = "[vf]", "[af]"
        print("\n⚠️ --speed applies to the WHOLE video, not selectively.")
    else:
        vmap, amap = "[v]", "[a]"

    cmd = ["ffmpeg", "-y", "-i", a.video, "-filter_complex", chain,
           "-map", vmap, "-map", amap,
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-c:a", "aac", "-b:a", "160k", a.write]
    print("\nwriting %s (%d segments)…" % (a.write, len(segs)))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr[-2500:], file=sys.stderr)
        return proc.returncode
    print("done: %s  (%s)" % (a.write, clock(duration(a.write))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
