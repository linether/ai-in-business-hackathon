# ComplaintGuard — telecom complaint escalation prevention

**Author:** @Genicayyy · **Date:** 09-12 17:36 AEST · **Track:** 1

## Where I know this from

During my internship at China Mobile, I listened to customer-service recordings to identify cases likely to escalate into formal complaints. I analysed why customers intended to escalate, classified the causes, and traced why the original complaint was not resolved in time. This proposal comes from that first-hand workflow.

No real customer recordings, phone numbers, internal tickets, or confidential employer data will be used.

## Who hurts

Complaint quality-assurance analysts and complaint operations managers in large telecom contact centres. They manually listen to recordings, reconstruct customer history, identify escalation risk, classify root causes, and explain which earlier handling failure allowed an ordinary complaint to escalate.

## What it costs them today

The exact figures still need validation:

    recordings reviewed per month
    × average minutes to listen and analyse each recording
    × analyst loaded hourly cost
    = manual review cost

Escalation also creates repeat calls, supervisor handling, specialist-team time, churn risk, and regulatory or reputational exposure.

Evidence source: first-hand observation during my China Mobile internship. Before pitching, I will estimate recordings reviewed per analyst per day, average review time, and the share requiring written root-cause analysis without disclosing confidential data.

## What we build

An AI system that analyses a telecom call and prior contact history, tracks unresolved customer needs and unfulfilled service promises, warns before an ordinary complaint escalates, and identifies the earliest missed intervention that could have prevented it.

## The demo the judges watch

1. Upload a reenacted telecom support call plus two synthetic prior-contact records.
2. The system transcribes the call and separates customer and agent speakers.
3. A timeline extracts the customer's needs: cancel an unexpected add-on, refund two months of charges, and receive confirmation today.
4. The agent explains the billing rule but does not address the refund or create the promised callback. ComplaintGuard marks those items unresolved.
5. On the third contact the customer mentions a regulator and switching providers. The escalation score rises from 34 to 89.
6. The screen explains the score: three repeat contacts, two unfulfilled promises, unresolved refund, external-complaint language, and churn intent.
7. It identifies the earliest preventable point: create and assign the refund case after contact one.
8. A dashboard groups synthetic cases by root cause: broken callback, insufficient authority, misunderstood need, repeated transfer, and policy gap.

The demo uses reenacted audio and synthetic CRM records. We will say that clearly.

## What it costs with our solution

Today, analysts listen to 100% of each selected recording and manually reconstruct the case. With ComplaintGuard, AI pre-analyses the case and analysts review the evidence, risk explanation, and uncertain fields.

We will measure review time on 20–30 labelled reenacted calls and report the observed reduction. We will not invent savings before running this test.

## Why this isn't a wrapper

Speech-to-text is commodity. Our engineering is the escalation-failure pipeline:

- speaker-aware transcription and segmentation;
- structured extraction of needs, constraints, promises, deadlines, and actions;
- multi-contact state tracking across calls and CRM events;
- semantic matching between requests and what the agent actually resolved;
- detection of unresolved needs and broken promises;
- risk fusion across lexical, behavioural, historical, and workflow signals;
- deterministic rules for repeat contact, missed deadlines, regulator mentions, and churn intent;
- evidence-grounded identification of the earliest preventable intervention;
- root-cause aggregation and a human-labelled evaluation harness.

LLMs perform judgement and extraction. Deterministic code handles scoring thresholds and consequential escalation rules so decisions are auditable.

## Existing alternatives

NiCE CXone Interaction Analytics, CallMiner, Observe.AI, Zendesk Intelligent Triage, and Salesforce Service Cloud offer combinations of transcription, topic and sentiment detection, quality assurance, routing, and interaction analytics.

Our difference is not generic sentiment analysis. ComplaintGuard reconstructs the failure chain:

    customer need → agent response → unresolved item → service promise
    → operational follow-through → repeat contact → escalation

It asks not only “is this customer angry?” but “which need is unresolved, which promise failed, and what was the earliest action that could have prevented escalation?”

## Hardest part

Correctly attributing why a complaint escalated. Strong emotion does not necessarily mean escalation, while a calm customer may go directly to a regulator.

Mitigations:

- treat emotion as one weak signal, not the decision;
- weight repeat contact, unresolved needs, broken promises, deadlines, regulator language, and churn intent more heavily;
- attach transcript evidence to every reason;
- allow a human reviewer to correct extracted facts;
- evaluate Mandarin wording and speaking styles separately;
- never use the score automatically to punish an agent or approve compensation.

## What we'd fake, and admit to

- reenacted calls, not confidential customer recordings;
- synthetic CRM history and service records;
- uploaded audio processed in chunks, not a carrier telephony integration;
- recommended actions only — no real refund, plan change, or regulatory workflow;
- a small telecom-specific taxonomy rather than production coverage.

## How we'd evaluate it

Create 20–30 reenacted scenarios labelled with customer needs, promises, deadlines, resolution status, whether escalation was warranted, root cause, and earliest preventable intervention.

Report need-extraction recall, unresolved-need F1, escalation precision and recall, root-cause accuracy, evidence-grounding accuracy, false-escalation rate, early-warning dialogue turns, and analyst review time with and without ComplaintGuard.

The key metric is not sentiment accuracy. It is whether the system finds a materially unresolved need early enough for a human to prevent escalation.

## Can we deploy it?

Yes. A web app can use uploaded audio, speech-to-text, a Python analysis API, structured LLM outputs, deterministic scoring, and synthetic contact history.

Build order:

1. upload and transcribe one reenacted call;
2. extract needs, promises, and actions;
3. show resolved versus unresolved items;
4. calculate and explain escalation risk;
5. add prior-contact history and earliest missed intervention;
6. add aggregate root-cause dashboard;
7. only then consider live microphone input.

## Self-score

| # | Question | Score |
|---|---|---:|
| 1 | Specific person named? | 2 |
| 2 | Hours × rate × volume? | 1 — first-hand source, exact figures needed |
| 3 | Real technical depth? | 2 |
| 4 | Demo path finishable? | 2 |
| 5 | Can name alternatives? | 2 |
| 6 | Off the obvious list? | 2 — analyst copilot, not a customer-facing chatbot |
| 7 | Deployable? | 2 |
| 8 | Ground truth to evaluate? | 2 |
| 9 | Survives cost/data/regulation? | 2 |
|  | **Total** | **17 / 18** |

## Decision requested from the team

Compare this against the education proposal on originality, first-hand evidence, technical risk, and how quickly we can label realistic cases. If selected, the first validation task is to quantify the current manual review workflow without using confidential China Mobile information.
