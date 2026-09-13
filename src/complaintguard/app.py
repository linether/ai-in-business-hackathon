"""FastAPI application — the thing a judge opens.

**Presentation is @Ranchelwood's area** (claimed on BOARD.md, 09-12 20:54). This
is a working, deliberately plain version so the system is demoable from the first
hour and there is something real to iterate on. Replace the template freely; the
route contract below is what the rest of the app depends on.

Routes:
    GET  /                      scenario picker
    GET  /case/{scenario_id}    full analysis
    GET  /api/case/{id}         the same analysis as JSON
    GET  /health                liveness, for the deploy check
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import pipeline, scenarios

# The scenario files use the team's working vocabulary, which is Chinese. The
# site is read by English-speaking judges, so display labels are mapped here
# rather than by rewriting the data — the taxonomy came from the teammate who
# did this job and it should stay in her words in the source.
CATEGORY_EN = {
    "计费争议": "billing dispute",
    "附加包未授权": "unauthorised add-on",
    "网络质量": "service quality",
    "套餐变更": "plan change",
    "退费": "refund",
    "服务态度": "conduct",
}
ROOT_CAUSE_EN = {
    "回电未兑现": "callback never made",
    "权限不足": "insufficient authority",
    "需求被误解": "need misread",
    "反复转接": "repeated transfers",
    "政策空白": "policy gap",
    "答复矛盾": "contradictory answers",
    "无人负责": "nobody assigned",
    "无": "",
}

BASE = Path(__file__).resolve().parent
AUDIO = Path(__file__).resolve().parents[2] / "data" / "audio"
templates = Jinja2Templates(directory=str(BASE / "templates"))

app = FastAPI(
    title="ComplaintGuard",
    description="Reconstructs why a complaint escalated, and the earliest point it could have been stopped.",
    version="0.1.0",
)


if AUDIO.is_dir():
    # Voiced with ElevenLabs from our own scripts. Served so a judge can hear the
    # calls rather than take our word for what the tone was.
    app.mount("/audio", StaticFiles(directory=str(AUDIO)), name="audio")


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "scenarios": len(scenarios.list_scenarios())})


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    cards = []
    for path in scenarios.list_scenarios():
        raw = scenarios.ground_truth(path)
        case = scenarios.load_case(path)
        first = case.contacts[0] if case.contacts else None
        cards.append(
            {
                "id": path.stem,
                "escalated": raw.get("should_escalate"),
                "category": CATEGORY_EN.get(raw.get("business_category", ""), ""),
                "root_cause": ROOT_CAUSE_EN.get(raw.get("root_cause", ""), ""),
                "contacts": len(case.contacts),
                "has_audio": (AUDIO / path.stem).is_dir(),
                # What the case is about, not why we wrote it — the internal test
                # rationale in the scenario file is for us, not for a judge.
                "note": first.summary if first else "",
            }
        )
    return templates.TemplateResponse("index.html", {"request": request, "cards": cards})


def _analyse(scenario_id: str):
    index_ = scenarios.scenario_index()
    if scenario_id not in index_:
        raise HTTPException(status_code=404, detail="No such scenario")
    path = index_[scenario_id]
    case = scenarios.load_case(path)
    return pipeline.analyse(case), scenarios.ground_truth(path)


@app.get("/case/{scenario_id}", response_class=HTMLResponse)
def case_view(request: Request, scenario_id: str) -> HTMLResponse:
    analysis, truth = _analyse(scenario_id)

    # Evidence is rendered with the line it cites, so a judge can click a reason
    # and land on the words that justify it. That traceability is the product.
    lines = {}
    for contact in analysis.case.contacts:
        if contact.transcript:
            lines[contact.seq] = contact.transcript.utterances

    # The failure chain, as a sequence of links the UI can draw. This is the
    # concept the whole product rests on, and until now it existed only as
    # prose. Each link says whether it held or broke, so the drawing shows where
    # the chain gave way rather than merely listing what happened.
    chain = _chain(analysis)

    # Per-utterance audio, if this scenario has been voiced. Keyed "seq-index"
    # so the template can ask for one line without knowing the filename rules.
    audio = {}
    case_audio = AUDIO / scenario_id
    if case_audio.is_dir():
        for contact in analysis.case.contacts:
            if not contact.transcript:
                continue
            for i, u in enumerate(contact.transcript.utterances):
                name = "{}-{:02d}-{}.mp3".format(contact.seq, i, u.speaker.value)
                if (case_audio / name).exists():
                    audio["{}-{}".format(contact.seq, i)] = "/audio/{}/{}".format(scenario_id, name)

    return templates.TemplateResponse(
        "case.html",
        {
            "request": request,
            "a": analysis,
            "truth": truth,
            "lines": lines,
            "scenario_id": scenario_id,
            "all_ids": [p.stem for p in scenarios.list_scenarios()],
            "audio": audio,
            "chain": chain,
            "category": CATEGORY_EN.get(truth.get("business_category", ""), ""),
            "root_cause": ROOT_CAUSE_EN.get(truth.get("root_cause", ""), ""),
        },
    )


def _chain(analysis):
    """Build the customer-need -> escalation chain for display.

    Deliberately derived from what the pipeline already found rather than from a
    second pass: if a link shows as broken here, some signal or claim upstream
    says so, and the panel below it carries the evidence.
    """
    case = analysis.case
    needs = [n for n in case.all_needs()]
    promises = [p for p in case.all_promises()]
    unresolved = [n for n in needs if n.status.value in ("unresolved", "partial")]
    broken = [p for p in promises if p.fulfilled is False or (p.overdue_by_hours or 0) > 0]
    kinds = {s.kind.value for s in analysis.risk.signals}

    links = [
        {"label": "Need raised", "note": needs[0].summary if needs else "—", "broke": False},
        {
            "label": "Agent acted",
            "note": "no owner assigned" if "no_owner" in kinds else "handled on the call",
            "broke": "no_owner" in kinds,
        },
        {
            "label": "Resolved",
            "note": unresolved[0].summary if unresolved else "nothing outstanding",
            "broke": bool(unresolved),
        },
    ]
    if promises:
        links.append({
            "label": "Promise kept",
            "note": broken[0].summary if broken else promises[0].summary,
            "broke": bool(broken),
        })
    links.append({
        "label": "Repeat contact",
        "note": "{} contacts".format(len(case.contacts)) if len(case.contacts) > 1 else "no repeat",
        "broke": "repeat_contact" in kinds,
    })
    links.append({
        "label": "Escalation",
        "note": ("regulator involved" if "regulator_mention" in kinds
                 else "avoided" if analysis.risk.score < 40 else "at risk"),
        "broke": analysis.risk.score >= 40,
    })
    return links


@app.get("/api/case/{scenario_id}")
def case_api(scenario_id: str) -> JSONResponse:
    analysis, _ = _analyse(scenario_id)
    return JSONResponse(analysis.model_dump(mode="json"))
