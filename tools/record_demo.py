"""Record the demo video: narrate with ElevenLabs, drive the site with Playwright, mux with ffmpeg.

    PYTHONPATH=src .venv/bin/python tools/record_demo.py --narrate   # generate voice-over
    PYTHONPATH=src .venv/bin/python tools/record_demo.py --record    # drive the browser
    PYTHONPATH=src .venv/bin/python tools/record_demo.py --mux       # combine into assets/

Order matters: narration first, because each scene waits exactly as long as its
line of voice-over takes. Measuring the audio and then pacing the browser to it
is what keeps picture and sound together without hand-timing anything.

The script is docs/demo-video.md, trimmed to what the site can actually show.
Nothing here narrates a capability we do not have — the site runs the
deterministic layers and does not call a model, and the voice-over says so.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "build" / "video"
SITE = os.environ.get("DEMO_SITE", "https://bizalchemists.duckdns.org")

# A calm, measured narrator. Same voice family as the corpus so the project
# sounds like one thing.
VOICE = os.environ.get("EL_VOICE_NARRATOR", "onwK4e9ZLuTAKqWW03F9")
MODEL = "eleven_multilingual_v2"

# Each scene: what is said, and what the browser does while it is said.
# "wait" is a floor — the real dwell time is the length of the narration.
SCENES: List[dict] = [
    {
        "id": "01-problem",
        "say": (
            "Last financial year, fifty-seven thousand telecommunications complaints reached the "
            "Australian Telecommunications Industry Ombudsman. In sixty percent of them, the issue "
            "was no or delayed action by the provider. Sixteen thousand came back to the Ombudsman "
            "after being referred to the telco, because the referral still didn't fix it. That is "
            "up thirty-seven percent in a year."
        ),
        "url": "/",
        "action": None,
    },
    {
        "id": "02-chain",
        "say": (
            "ComplaintGuard reads a customer's calls and reconstructs the chain. What they asked "
            "for. What the agent committed to. Where it broke. This case escalated, and you can see "
            "where the chain gave way before reading a single number."
        ),
        "url": "/case/demo-001",
        "action": "scroll_chain",
    },
    {
        "id": "03-intervention",
        "say": (
            "On the third of September the agent promised a callback within twenty-four hours. It "
            "never happened. The customer rang twice more. The earliest point this could have been "
            "stopped was the twenty-four hour mark on the fourth. Every existing tool gives you a "
            "risk score, or root causes across a quarter. None of them tells you when this one "
            "could still have been caught."
        ),
        "url": None,
        "action": "scroll_intervention",
    },
    {
        "id": "04-evidence",
        "say": (
            "Every reason carries the line it came from. Click it, and you land on the words the "
            "agent actually said. That matters, because this system can claim an agent promised "
            "something. If it is wrong about that, it blames a real person. So every quote is "
            "checked verbatim against the transcript, by plain string comparison, with no model "
            "involved."
        ),
        "url": None,
        "action": "click_evidence",
    },
    {
        "id": "05-angry",
        "say": (
            "This customer is furious. They are shouting, they interrupt, they have been charged "
            "twice. Risk score: zero. The agent reversed the charge during the call. Nothing is "
            "outstanding, and the chain is unbroken."
        ),
        "url": "/case/demo-002",
        "action": "scroll_chain",
    },
    {
        "id": "06-calm",
        "say": (
            "This customer never raises their voice. Risk score: one hundred. They asked the same "
            "question twice, got two different answers, were told to prove it themselves, and have "
            "already lodged with the Ombudsman. Any system built on sentiment gets both of these "
            "backwards. We track unresolved needs and unmet commitments, not tone."
        ),
        "url": "/case/demo-003",
        "action": "scroll_chain",
    },
    {
        "id": "065-subtle",
        "say": (
            "One more, because it is the case a simpler system misses entirely. Here the agent "
            "promised a callback within forty-eight hours, and delivered it, exactly on time. The "
            "promise was kept. But the callback carried no outcome, no ticket was ever raised, and "
            "nobody was assigned. A system watching only promises sees nothing wrong here. The chain "
            "shows where it actually broke: the problem was never given an owner."
        ),
        "url": "/case/demo-004",
        "action": "scroll_chain",
    },
    {
        "id": "07-honest",
        "say": (
            "Everything here is synthetic. We wrote the call scripts and voiced them with "
            "ElevenLabs, which is also why we have exact ground truth. The deployed site runs the "
            "deterministic layers only and does not call a model. The language model extraction "
            "runs in our evaluation, measured on transcripts with nothing pre-answered: escalation "
            "F1 of ninety-three percent, and zero citation failures across eighty-three quotes. The "
            "failure that would put words in a real agent's mouth did not happen once. We are "
            "BizAlchemists."
        ),
        "url": "/",
        "action": None,
    },
]


def narrate() -> None:
    import httpx

    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise SystemExit("ELEVENLABS_API_KEY is not set — see docs/resources.md")

    out = WORK / "audio"
    out.mkdir(parents=True, exist_ok=True)
    total = 0
    for scene in SCENES:
        path = out / "{}.mp3".format(scene["id"])
        if path.exists():
            print("  {}  cached".format(scene["id"]))
            continue
        resp = httpx.post(
            "https://api.elevenlabs.io/v1/text-to-speech/{}".format(VOICE),
            headers={"xi-api-key": key, "content-type": "application/json"},
            json={
                "text": scene["say"],
                "model_id": MODEL,
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.7, "speed": 0.94},
            },
            timeout=180,
        )
        resp.raise_for_status()
        path.write_bytes(resp.content)
        total += len(scene["say"])
        print("  {}  {:,} bytes  ({} chars)".format(scene["id"], len(resp.content), len(scene["say"])))
    print("narration done, ~{:,} credits used this run".format(total))


def _durations() -> List[float]:
    """How long each line of narration runs, so the browser can match it."""
    out = []
    for scene in SCENES:
        path = WORK / "audio" / "{}.mp3".format(scene["id"])
        if not path.exists():
            raise SystemExit("missing narration for {} — run --narrate first".format(scene["id"]))
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, check=True,
        )
        out.append(float(probe.stdout.strip()))
    return out


def record() -> None:
    from playwright.sync_api import sync_playwright

    durations = _durations()
    video_dir = WORK / "raw"
    video_dir.mkdir(parents=True, exist_ok=True)
    for old in video_dir.glob("*.webm"):
        old.unlink()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir=str(video_dir),
            record_video_size={"width": 1280, "height": 800},
            device_scale_factor=2,
        )
        page = ctx.new_page()
        page.goto(SITE + "/", wait_until="networkidle")

        for scene, seconds in zip(SCENES, durations):
            if scene["url"]:
                page.goto(SITE + scene["url"], wait_until="networkidle")
            page.wait_for_timeout(500)

            act = scene["action"]
            if act == "scroll_chain":
                page.evaluate("window.scrollTo({top: 120, behavior: 'smooth'})")
            elif act == "scroll_intervention":
                page.evaluate(
                    "document.querySelector('.intervene')"
                    "?.scrollIntoView({block:'center', behavior:'smooth'})"
                )
            elif act == "click_evidence":
                page.evaluate(
                    "document.querySelectorAll('.panel')[2]"
                    "?.scrollIntoView({block:'start', behavior:'smooth'})"
                )
                page.wait_for_timeout(1800)
                link = page.query_selector(".sig .quote a")
                if link:
                    link.click()
                    page.wait_for_timeout(1200)

            # Hold the shot for as long as the voice-over runs, plus a beat.
            page.wait_for_timeout(int(seconds * 1000) - 500 + 600)
            print("  {}  held {:.1f}s".format(scene["id"], seconds))

        page.wait_for_timeout(800)
        ctx.close()
        browser.close()

    made = sorted(video_dir.glob("*.webm"))
    print("recorded: {}".format(made[0].name if made else "nothing"))


def mux() -> None:
    videos = sorted((WORK / "raw").glob("*.webm"))
    if not videos:
        raise SystemExit("no recording found — run --record first")

    concat = WORK / "narration.txt"
    concat.write_text(
        "\n".join("file '{}'".format((WORK / 'audio' / (s['id'] + '.mp3')).as_posix())
                  for s in SCENES),
        encoding="utf-8",
    )
    voice = WORK / "narration.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(voice)],
        check=True, capture_output=True,
    )

    out = ROOT / "assets" / "demo.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(videos[0]), "-i", str(voice),
         "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)],
        check=True, capture_output=True,
    )

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(out)],
        capture_output=True, text=True, check=True,
    )
    secs = float(probe.stdout.strip())
    print("wrote {}  {:.0f}s  {:,} bytes".format(out, secs, out.stat().st_size))
    if not 180 <= secs <= 300:
        print("!! {:.0f}s is outside the required 3-5 minutes".format(secs))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--narrate", action="store_true")
    ap.add_argument("--record", action="store_true")
    ap.add_argument("--mux", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.all or a.narrate:
        narrate()
    if a.all or a.record:
        record()
    if a.all or a.mux:
        mux()
    if not any([a.all, a.narrate, a.record, a.mux]):
        ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
