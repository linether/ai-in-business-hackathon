"""Evaluation harness.

Run:  PYTHONPATH=src .venv/bin/python notebooks/evaluate.py

Reports three separate failure rates rather than one accuracy number, because
hallucination is not one failure mode. Current practice distinguishes factual,
grounding, citation and reasoning failures, each needing its own detector — see
docs/architecture-upgrade.md.

    citation   the quote does not appear verbatim in the line it cites
               -> pure string comparison, no model involved
    grounding  a claim the system made has no counterpart in the script
               -> we wrote the scripts, so anything extra is invented
    reasoning  the claim is real but its status was judged wrong
               -> e.g. a promise that was kept, scored as broken

Plus the two decisions that actually matter to a user:

    escalation    should this case have been escalated?
    intervention  which contact was the last chance to stop it?

**Matching is by utterance index, never by a model judging whether two
extractions mean the same thing.** Using an LLM to grade an LLM is circular, and
the panel includes a statistics PhD and an evaluation specialist who will ask
exactly how correctness was decided.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from complaintguard import pipeline, scenarios  # noqa: E402
from complaintguard.models import Confidence  # noqa: E402
from complaintguard.pipeline import citation  # noqa: E402

ESCALATE_AT = 40  # risk band boundary; see pipeline/risk.py


@dataclass
class Counts:
    tp: int = 0
    fp: int = 0
    fn: int = 0

    @property
    def precision(self) -> Optional[float]:
        d = self.tp + self.fp
        return self.tp / d if d else None

    @property
    def recall(self) -> Optional[float]:
        d = self.tp + self.fn
        return self.tp / d if d else None

    @property
    def f1(self) -> Optional[float]:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if p and r else None


@dataclass
class Report:
    promises: Counts = field(default_factory=Counts)
    needs: Counts = field(default_factory=Counts)
    escalation: Counts = field(default_factory=Counts)
    intervention_right: int = 0
    intervention_total: int = 0
    citations_checked: int = 0
    citations_failed: int = 0
    claims_total: int = 0
    claims_ungrounded: int = 0
    status_checked: int = 0
    status_wrong: int = 0
    rows: List[Tuple[str, str, str]] = field(default_factory=list)


def _pct(x: Optional[float]) -> str:
    return "—" if x is None else "{:.0%}".format(x)


def _keys(items) -> Dict[Tuple[int, Optional[int]], object]:
    """Key a claim by (contact, utterance index) — the exact anchor."""
    out = {}
    for it in items:
        ev = list(getattr(it, "evidence", []))
        if not ev:
            continue
        out[(ev[0].contact_seq, ev[0].utterance_index)] = it
    return out


def evaluate() -> Report:
    rep = Report()

    for path in scenarios.list_scenarios():
        truth_case = scenarios.load_case(path)  # labels intact
        gt = scenarios.ground_truth(path)

        analysis = pipeline.analyse(scenarios.load_case(path))
        case = analysis.case

        # --- citation: does every quote exist verbatim where it says it does
        for contact in case.contacts:
            if not contact.extraction:
                continue
            for claim in (
                list(contact.extraction.needs)
                + list(contact.extraction.promises)
                + list(contact.extraction.actions)
            ):
                for ev in list(getattr(claim, "evidence", [])) + list(
                    getattr(claim, "resolution_evidence", [])
                ):
                    rep.citations_checked += 1
                    if not citation.check_evidence(case, ev):
                        rep.citations_failed += 1

        # --- grounding + extraction P/R, keyed by utterance index
        for label_c, out_c in zip(truth_case.contacts, case.contacts):
            for kind, counts in (("promises", rep.promises), ("needs", rep.needs)):
                want = _keys(getattr(label_c.extraction, kind) if label_c.extraction else [])
                got = _keys(getattr(out_c.extraction, kind) if out_c.extraction else [])
                for k in got:
                    rep.claims_total += 1
                    if k in want:
                        counts.tp += 1
                    else:
                        counts.fp += 1
                        rep.claims_ungrounded += 1  # invented: not in the script
                for k in want:
                    if k not in got:
                        counts.fn += 1

                # --- reasoning: right claim, wrong status
                for k, out_item in got.items():
                    if k not in want:
                        continue
                    rep.status_checked += 1
                    ref = want[k]
                    if kind == "promises":
                        wrong = out_item.fulfilled != ref.fulfilled
                    else:
                        wrong = out_item.status != ref.status
                    if wrong and out_item.confidence is not Confidence.UNCERTAIN:
                        rep.status_wrong += 1

        # --- escalation decision
        predicted = analysis.risk.score >= ESCALATE_AT
        expected = bool(gt.get("should_escalate"))
        if predicted and expected:
            rep.escalation.tp += 1
        elif predicted and not expected:
            rep.escalation.fp += 1
        elif expected and not predicted:
            rep.escalation.fn += 1

        # --- earliest intervention point
        exp_ip = gt.get("earliest_intervention_contact_seq")
        got_ip = analysis.earliest_intervention.contact_seq if analysis.earliest_intervention else None
        rep.intervention_total += 1
        hit = got_ip == exp_ip
        rep.intervention_right += int(hit)

        rep.rows.append(
            (
                case.case_id,
                "{:>3}  {}".format(
                    analysis.risk.score, "ok " if predicted == expected else "MISS"
                ),
                "{} vs {}  {}".format(got_ip, exp_ip, "ok" if hit else "MISS"),
            )
        )

    return rep


def main() -> int:
    r = evaluate()

    print("\nComplaintGuard evaluation")
    print("=" * 62)
    print("{} scenarios\n".format(r.intervention_total))

    print("per case")
    print("-" * 62)
    print("{:<12}{:<22}{}".format("case", "risk / escalation", "intervention contact"))
    for cid, esc, ip in r.rows:
        print("{:<12}{:<22}{}".format(cid, esc, ip))

    print("\nthe two decisions that matter")
    print("-" * 62)
    print("escalation        precision {}   recall {}   f1 {}".format(
        _pct(r.escalation.precision), _pct(r.escalation.recall), _pct(r.escalation.f1)))
    print("intervention      accuracy {:.0%}  ({}/{})".format(
        r.intervention_right / r.intervention_total, r.intervention_right, r.intervention_total))

    print("\nextraction")
    print("-" * 62)
    for name, c in (("promises", r.promises), ("needs", r.needs)):
        print("{:<18}precision {}   recall {}   f1 {}".format(
            name, _pct(c.precision), _pct(c.recall), _pct(c.f1)))

    print("\nfailure modes, reported separately")
    print("-" * 62)
    cit = r.citations_failed / r.citations_checked if r.citations_checked else 0
    gnd = r.claims_ungrounded / r.claims_total if r.claims_total else 0
    rsn = r.status_wrong / r.status_checked if r.status_checked else 0
    print("citation   {:>6.1%}   {}/{} quotes not found verbatim where cited".format(
        cit, r.citations_failed, r.citations_checked))
    print("grounding  {:>6.1%}   {}/{} claims with no counterpart in the script".format(
        gnd, r.claims_ungrounded, r.claims_total))
    print("reasoning  {:>6.1%}   {}/{} real claims given the wrong status".format(
        rsn, r.status_wrong, r.status_checked))

    print("\n" + "=" * 62)
    print("NOTE: run against the labelled stub extractor, which reads the answers.")
    print("These numbers measure the deterministic layers only. They become a real")
    print("measurement of the system the moment LLMExtractor replaces it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
