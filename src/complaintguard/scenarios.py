"""Load scenario JSON into the Case model.

Scenarios live in data/scenarios/. They are synthetic and carry their own ground
truth, because we wrote the scripts — see data/scenarios/README.md.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from .models import (
    Action,
    Case,
    Channel,
    Contact,
    Evidence,
    Extraction,
    Need,
    NeedStatus,
    Promise,
    Speaker,
    Transcript,
    Utterance,
)

SCENARIO_DIR = Path(__file__).resolve().parents[2] / "data" / "scenarios"


def _evidence(raw: List[dict]) -> List[Evidence]:
    return [Evidence(**e) for e in raw or []]


def _load_extraction(raw: Optional[dict], seq: int) -> Optional[Extraction]:
    if not raw:
        return None
    needs = [
        Need(
            id=n["id"],
            utterance_index=n.get("utterance_index"),
            summary=n["summary"],
            raised_at=n["raised_at"],
            status=NeedStatus(n.get("status", "unknown")),
            evidence=_evidence(n.get("evidence")),
            resolution_note=n.get("resolution_note"),
            resolution_evidence=_evidence(n.get("resolution_evidence")),
            service_affected=n.get("service_affected"),
        )
        for n in raw.get("needs", [])
    ]
    promises = [
        Promise(
            id=p["id"],
            utterance_index=p.get("utterance_index"),
            summary=p["summary"],
            made_at=p["made_at"],
            due_at=p.get("due_at"),
            fulfilled=p.get("fulfilled"),
            evidence=_evidence(p.get("evidence")),
        )
        for p in raw.get("promises", [])
    ]
    actions = [
        Action(
            id=a["id"],
            utterance_index=a.get("utterance_index"),
            summary=a["summary"],
            taken_at=a["taken_at"],
            evidence=_evidence(a.get("evidence")),
            assigns_owner=a.get("assigns_owner"),
            contradicts=a.get("contradicts"),
        )
        for a in raw.get("actions", [])
    ]
    return Extraction(contact_seq=seq, needs=needs, promises=promises, actions=actions)


def load_case(path: Path, with_labels: bool = True) -> Case:
    """Build a Case from a scenario file.

    with_labels=False strips the extraction, which is what the real pipeline sees:
    transcripts only, nothing pre-answered. Use that once the LLM extractor exists.
    """
    raw = json.loads(path.read_text(encoding="utf-8"))
    contacts: List[Contact] = []
    for c in raw["contacts"]:
        t = c.get("transcript")
        transcript = (
            Transcript(
                contact_seq=c["seq"],
                language=t.get("language", "en"),
                utterances=[
                    Utterance(
                        start_s=u["start_s"],
                        end_s=u["end_s"],
                        speaker=Speaker(u["speaker"]),
                        text=u["text"],
                    )
                    for u in t["utterances"]
                ],
            )
            if t
            else None
        )
        contacts.append(
            Contact(
                seq=c["seq"],
                occurred_at=c["occurred_at"],
                channel=Channel(c.get("channel", "call")),
                summary=c.get("summary", ""),
                transcript=transcript,
                extraction=_load_extraction(c.get("extraction"), c["seq"]) if with_labels else None,
            )
        )
    return Case(case_id=raw["case_id"], customer_ref=raw.get("customer_ref", ""), contacts=contacts)


def ground_truth(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")).get("ground_truth", {})


def list_scenarios() -> List[Path]:
    return sorted(SCENARIO_DIR.glob("demo-*.json"))


def scenario_index() -> Dict[str, Path]:
    return {p.stem: p for p in list_scenarios()}
