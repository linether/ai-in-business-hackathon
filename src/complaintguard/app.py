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
    GET  /try                   paste a transcript
    POST /try                   analyse it live
    GET  /live                  a call you can hold, watched as it happens
    POST /live/start|turn|watch the room's API
    GET  /policy/{slug}         the written rule behind a finding
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import conversation, knowledge, live, pipeline, scenarios
from .pipeline.extract import LLMExtractor

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
        # Three states, not two. The prepared cases carry a label so a promise is
        # always kept or broken, but a pasted transcript often ends before anyone
        # could follow through — and drawing an open promise as "kept" would be
        # the system asserting something nobody said.
        if broken:
            links.append({"label": "Promise kept", "note": broken[0].summary, "broke": True})
        elif any(p.fulfilled is None for p in promises):
            open_ = next(p for p in promises if p.fulfilled is None)
            links.append({"label": "Promise open", "note": open_.summary,
                          "broke": False, "mark": "○"})
        else:
            links.append({"label": "Promise kept", "note": promises[0].summary, "broke": False})
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


# --------------------------------------------------------------------------
# The "try it yourself" path.
#
# Deliberately quarantined: it imports nothing the four routes above depend on,
# every failure inside it is caught and rendered as a message, and if it were
# deleted the prepared cases would behave identically. It is the only place on
# the site that spends money, so it is also the only place with limits — see
# live.py for the reasoning behind them.
# --------------------------------------------------------------------------


def _try_context(request: Request, **extra) -> dict:
    left, total = live.budget_left()
    ctx = {
        "request": request,
        "max_chars": live.MAX_CHARS,
        "max_lines": live.MAX_LINES,
        "per_ip": live.PER_IP_PER_HOUR,
        "left": left,
        "total": total,
        "open_": live.configured() and left > 0,
        "sample": live.SAMPLE,
        "submitted": "",
        "error": "",
    }
    ctx.update(extra)
    return ctx


@app.get("/try", response_class=HTMLResponse)
def try_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("try.html", _try_context(request))


@app.post("/try", response_class=HTMLResponse)
def try_run(request: Request, transcript: str = Form("")) -> HTMLResponse:
    """Parse, budget-check, analyse, render — and return the form on any failure.

    There is no error page and no 500 here on purpose. A visitor who pastes
    something odd, or arrives after the day's budget is gone, should get a
    sentence they can act on and a working form, not a stack trace.
    """
    client_ip = live.visitor_ip(request)

    try:
        case = live.parse_transcript(transcript)
    except live.LiveError as exc:
        return templates.TemplateResponse(
            "try.html", _try_context(request, error=str(exc), submitted=transcript)
        )

    key = live.cache_key(transcript)
    analysis = live.cached(key)

    if analysis is None:
        try:
            live.check_budget(client_ip)
            llm = live.client()
        except live.LiveError as exc:
            return templates.TemplateResponse(
                "try.html", _try_context(request, error=str(exc), submitted=transcript)
            )
        try:
            analysis = pipeline.analyse(case, extractor=LLMExtractor(llm), resolver=llm)
        except Exception:  # noqa: BLE001 — provider errors, timeouts, bad JSON
            return templates.TemplateResponse(
                "try.html",
                _try_context(
                    request,
                    error="The model call did not come back cleanly. Try again, or open one of "
                          "the prepared cases — those run without a model and never fail this way.",
                    submitted=transcript,
                ),
            )
        live.spend(client_ip)
        live.remember(key, analysis)

    lines = {c.seq: c.transcript.utterances for c in analysis.case.contacts if c.transcript}
    return templates.TemplateResponse(
        "case.html",
        {
            "request": request,
            "a": analysis,
            "truth": {},
            "lines": lines,
            "scenario_id": "your transcript",
            "all_ids": [],
            "audio": {},
            "chain": _chain(analysis),
            "category": "",
            "root_cause": "",
            "live": True,
        },
    )


# --------------------------------------------------------------------------
# The live room.
#
# Quarantined like /try, and for the same reason: it is the only other place
# that spends money, and nothing above imports it. The conversation is a demo
# prop — what is being submitted is the supervisor watching it. The page says so
# in as many words, because a bot that talks to customers is a product category
# with a dozen incumbents and this is not that.
#
# The budget is charged at /live/start, never on a page view, so a judge opening
# the page and reading it costs nothing.
# --------------------------------------------------------------------------


def _room_context(request: Request, **extra) -> dict:
    left, total = conversation.budget_left()
    ctx = {
        "request": request,
        "open_": conversation.room_open() and left > 0 and live.configured(),
        "closed_reason": (
            "" if conversation.room_open()
            else "The live room is switched off right now. It is opened for judging and while we "
                 "are testing, because every turn spends transcription and speech credits."
        ),
        "left": left,
        "total": total,
        "max_turns": conversation.MAX_TURNS,
        "openers": conversation.OPENERS,
        "policies": [
            {"slug": c.slug, "ref": c.ref, "title": c.title}
            for c in knowledge.corpus().chunks
        ],
    }
    ctx.update(extra)
    return ctx


@app.get("/live", response_class=HTMLResponse)
def room(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("live.html", _room_context(request))


@app.post("/live/start")
def room_start(request: Request) -> JSONResponse:
    ip = live.visitor_ip(request)
    try:
        session = conversation.start(ip)
    except conversation.RoomError as exc:
        return JSONResponse({"ok": False, "error": str(exc)}, status_code=200)
    left, _ = conversation.budget_left()
    return JSONResponse({"ok": True, "session": session.id, "turns_left": session.turns_left,
                         "calls_left_today": left})


@app.post("/live/turn")
def room_turn(request: Request, session: str = Form(""), text: str = Form("")) -> JSONResponse:
    """One turn. Never raises — a failure here must not end the call."""
    try:
        sess = conversation.get(session)
        out = conversation.reply(sess, text, live.client(json_mode=False, timeout=30))
    except conversation.RoomError as exc:
        return JSONResponse({"ok": False, "error": str(exc)}, status_code=200)
    except Exception:  # noqa: BLE001 — provider errors, timeouts, malformed replies
        return JSONResponse(
            {"ok": False,
             "error": "The agent did not answer that one. Say it again — this turn was not counted."},
            status_code=200,
        )
    out["ok"] = True
    return JSONResponse(out)


@app.post("/live/watch")
def room_watch(request: Request, session: str = Form("")) -> JSONResponse:
    """The supervisor, a beat behind. Purely additive — if it fails, the call goes on."""
    try:
        sess = conversation.get(session)
        return JSONResponse({"ok": True, **conversation.watch(sess, live.client())})
    except conversation.RoomError as exc:
        return JSONResponse({"ok": False, "error": str(exc)}, status_code=200)
    except Exception:  # noqa: BLE001
        return JSONResponse({"ok": False, "error": "watch failed"}, status_code=200)


@app.get("/policy/{slug}", response_class=HTMLResponse)
def policy(request: Request, slug: str) -> HTMLResponse:
    """The rule behind a finding, so a supervisor can disagree with us."""
    chunk = knowledge.corpus().by_slug(slug)
    if chunk is None:
        raise HTTPException(status_code=404, detail="No such policy")
    return templates.TemplateResponse(
        "policy.html",
        {"request": request, "chunk": chunk, "all": knowledge.corpus().chunks},
    )


@app.get("/live/say/{digest}")
def room_voice(digest: str):
    """Serve one synthesised agent line. Cached by its own text, so this is free."""
    from fastapi.responses import FileResponse

    path = conversation.voice_path(digest)
    if path is None:
        raise HTTPException(status_code=404, detail="No such line")
    return FileResponse(str(path), media_type="audio/mpeg")


@app.post("/live/hear")
async def room_hear(request: Request) -> JSONResponse:
    """Transcribe one spoken turn and answer it — the whole turn, in one trip.

    Split from /live/turn only by how the visitor's words arrive. Everything
    after transcription is the same code, so speaking and typing cannot drift
    apart, and a browser with no microphone loses nothing but the microphone.
    """
    form = await request.form()
    session_id = str(form.get("session") or "")
    upload = form.get("audio")

    try:
        sess = conversation.get(session_id)
        if upload is None or not hasattr(upload, "read"):
            raise conversation.RoomError("No audio arrived. Type the turn instead.")
        blob = await upload.read()
        text = conversation.hear(blob, getattr(upload, "filename", "turn.webm") or "turn.webm")
        out = conversation.reply(sess, text, live.client(json_mode=False, timeout=30))
    except conversation.RoomError as exc:
        return JSONResponse({"ok": False, "error": str(exc)}, status_code=200)
    except Exception:  # noqa: BLE001
        return JSONResponse(
            {"ok": False,
             "error": "That turn did not get through. Say it again, or type it — "
                      "it was not counted."},
            status_code=200,
        )
    out["ok"] = True
    return JSONResponse(out)
