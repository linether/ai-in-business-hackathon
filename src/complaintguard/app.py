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
from fastapi.templating import Jinja2Templates

from . import pipeline, scenarios

BASE = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE / "templates"))

app = FastAPI(
    title="ComplaintGuard",
    description="Reconstructs why a complaint escalated, and the earliest point it could have been stopped.",
    version="0.1.0",
)


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "scenarios": len(scenarios.list_scenarios())})


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    cards = []
    for path in scenarios.list_scenarios():
        raw = scenarios.ground_truth(path)
        cards.append(
            {
                "id": path.stem,
                "escalated": raw.get("should_escalate"),
                "category": raw.get("business_category", "—"),
                "root_cause": raw.get("root_cause", "—"),
                "note": raw.get("why_this_scenario_exists", ""),
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

    return templates.TemplateResponse(
        "case.html",
        {
            "request": request,
            "a": analysis,
            "truth": truth,
            "lines": lines,
            "scenario_id": scenario_id,
            "all_ids": [p.stem for p in scenarios.list_scenarios()],
        },
    )


@app.get("/api/case/{scenario_id}")
def case_api(scenario_id: str) -> JSONResponse:
    analysis, _ = _analyse(scenario_id)
    return JSONResponse(analysis.model_dump(mode="json"))
