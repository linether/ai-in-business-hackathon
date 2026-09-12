"""Transcribe audio with ElevenLabs Scribe — layer 2.

    PYTHONPATH=src python -m complaintguard.audio.stt --dry-run recording.mp3
    PYTHONPATH=src python -m complaintguard.audio.stt recording.mp3

⚠️ **Never run against the live API** — no key was available when this was
written. Treat the first real call as a test.

Two things Scribe gives us that the whole design depends on:

    diarize=true                 separates customer from agent
    timestamps_granularity=word  word-level offsets

The word offsets are not a nicety. Every claim the system makes carries the line
it came from, and a judge can click a reason to land on the words behind it —
that traceability is the product, and it is built on these timestamps.

**Results are cached to data/transcripts/ and the cache is always checked first.**
Speech-to-text runs around 330 credits a minute against a 121,000/month
allowance, so re-transcribing the same file while debugging is how a team loses
its budget in an afternoon.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

import httpx

from ..models import Speaker, Transcript, Utterance

API = "https://api.elevenlabs.io/v1/speech-to-text"
CACHE_DIR = Path(__file__).resolve().parents[3] / "data" / "transcripts"
MODEL = os.environ.get("EL_STT_MODEL", "scribe_v2")

# Scribe returns speaker_0 / speaker_1 without knowing which is which. In these
# recordings the customer speaks first, so speaker_0 is the customer. If that
# assumption ever breaks, this is the one line to change.
SPEAKER_ORDER = [Speaker.CUSTOMER, Speaker.AGENT]


def _key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise SystemExit(
            "ELEVENLABS_API_KEY is not set. See docs/resources.md for how to claim it.\n"
            "Use --dry-run to check the plan without a key."
        )
    return key


def _cache_path(audio: Path) -> Path:
    digest = hashlib.sha256(audio.read_bytes()).hexdigest()[:16]
    return CACHE_DIR / "{}-{}.json".format(audio.stem, digest)


def transcribe_raw(audio: Path, num_speakers: int = 2, language: Optional[str] = None) -> dict:
    """Call Scribe, or return the cached response if this exact file was done before."""
    cached = _cache_path(audio)
    if cached.exists():
        return json.loads(cached.read_text(encoding="utf-8"))

    data = {
        "model_id": MODEL,
        "diarize": "true",
        "num_speakers": str(num_speakers),
        "timestamps_granularity": "word",
        # entity_detection carries a 30% surcharge and we transcribe synthetic
        # scripts, so there is no PII to find. Leave it off.
    }
    if language:
        data["language_code"] = language

    with audio.open("rb") as fh:
        resp = httpx.post(
            API,
            headers={"xi-api-key": _key()},
            data=data,
            files={"file": (audio.name, fh, "application/octet-stream")},
            timeout=600,
        )
    resp.raise_for_status()
    payload = resp.json()

    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def to_transcript(payload: dict, contact_seq: int = 1) -> Transcript:
    """Group Scribe's word stream into utterances.

    The API returns words, not turns. A turn ends when the speaker changes, so
    the grouping is a fold over the word list rather than anything clever.
    """
    words = [w for w in payload.get("words", []) if w.get("type") == "word"]
    speakers = sorted({w.get("speaker_id") for w in words if w.get("speaker_id")})
    mapping: Dict[str, Speaker] = {
        sid: SPEAKER_ORDER[i] if i < len(SPEAKER_ORDER) else Speaker.UNKNOWN
        for i, sid in enumerate(speakers)
    }

    utterances: List[Utterance] = []
    current: Optional[dict] = None
    for w in words:
        who = mapping.get(w.get("speaker_id"), Speaker.UNKNOWN)
        if current is None or current["speaker"] is not who:
            if current:
                utterances.append(Utterance(**{**current, "text": current["text"].strip()}))
            current = {"speaker": who, "start_s": w.get("start", 0.0),
                       "end_s": w.get("end", 0.0), "text": ""}
        current["text"] += w.get("text", "") + " "
        current["end_s"] = w.get("end", current["end_s"])
    if current:
        utterances.append(Utterance(**{**current, "text": current["text"].strip()}))

    return Transcript(
        contact_seq=contact_seq,
        language=payload.get("language_code", "en"),
        utterances=utterances,
    )


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("audio", nargs="+", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--language", default=None, help="ISO code; omit to auto-detect")
    args = ap.parse_args(argv)

    for path in args.audio:
        if not path.exists():
            print("  ! missing: {}".format(path), file=sys.stderr)
            continue
        cached = _cache_path(path)
        mb = path.stat().st_size / 1_000_000
        if args.dry_run:
            print("{}  {:.1f} MB  {}".format(
                path.name, mb, "CACHED — no call, no credits" if cached.exists() else "would call Scribe"))
            continue

        payload = transcribe_raw(path, language=args.language)
        transcript = to_transcript(payload)
        print("{}  {} utterances  {:.0f}s  cache: {}".format(
            path.name, len(transcript.utterances),
            payload.get("audio_duration_secs", 0), cached.name))
        for u in transcript.utterances[:3]:
            print("   [{}] {}".format(u.speaker.value, u.text[:70]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
