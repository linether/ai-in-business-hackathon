# Track analysis — which one, and why

Written against the official track text ([brief.md](brief.md)), the 100-point rubric
([judging.md](judging.md)) and what the sponsor said wins ([keynote.md](keynote.md)).

## First, the mechanics most teams get wrong

**The track label is a Monday decision, not a Saturday one.** Submission Requirements say only:
*"Track Name: please include in the description which track you are submitting to."* You declare it in
the Devpost description at submission time. Nothing stops you building first and labelling last.

**The big prizes are not per-track.** 1st $2,000 / 2nd $500 / 3rd $200 are overall; each track carries a
separate **$100**. So the track you pick moves $100 and your framing — it does not move the $2,000.
**Do not spend Saturday afternoon arguing about tracks.** Spend it picking the problem.

**The ElevenLabs special track is the one place track choice has real expected value.** It is a separate
prize with its own judging, and the field is only teams that use voice meaningfully. You must be in one
of tracks 1–3 anyway, so entering is pure addition — *if* voice is genuinely core.

**Tracks 1 and 3 overlap almost completely.** Nearly any project can be framed either way. Track 1 is
process-first framing ("businesses do X, we made X better"); Track 3 is problem-first framing ("here is
a painful problem, here is our attack"). Pick the framing that makes your project look sharpest.

## Track 1 — Improve an Existing Business Capability

**Official:** take something a business already does and make it significantly better with AI — faster,
cheaper, more accurate, more scalable, easier to use. Augmenting, not inventing.

**Their examples:** end-to-end customer support agent · document processing for invoices and contracts ·
AI coding/QA system · lead-researching sales assistant · multimodal inventory management · internal
knowledge agent that takes actions · demand forecasting and scheduling.

**Where it scores well**

- *Impact & Value Proposition (9)* — **the easiest track to quantify.** The process already exists, so
  there is a real baseline: hours × rate × volume. This is exactly the sponsor's "52 minutes → 30
  seconds" and "104 hours a month" framing.
- *Feasibility & Viability (8)* — someone already does this job, so the adoption path is obvious.
- *Functionality (10)* — a narrow existing process is the most achievable thing to actually finish in 48h.
- *Problem Significance (8)* — the pain is pre-validated; you don't have to argue anyone wants it.
- *Use of Data/Models (6)* — a real baseline means you can actually **evaluate** against ground truth.

**Where it bleeds points**

- *Originality (10)* — **this is the trap.** Their own example list is the default hackathon project set,
  and each one is an existing commercial product: support agents (Sierra, Intercom Fin), invoice
  processing (Rossum, Docsumo), lead qualification (Clay, Apollo). The rubric gives **0–4 for "a direct
  clone of an existing well-known product with no meaningful change."**
- *Differentiation (7)* — your competitors are famous, numerous and better funded. Hard to argue you're
  better after 48 hours.

**Verdict:** the highest-floor track and the sponsor's own mental model — all four of his case studies
live here. But if you pick one of *their* listed examples you walk straight into the originality trap.
**Take Track 1's discipline and point it at a process nobody at this hackathon will think of.**

## Track 2 — Create a New Business Capability

**Official:** build something a business previously could not realistically do. New product, service,
workflow, interface or organisational capability, via agents, multimodal, voice, vision, generative
systems, autonomous workflows.

**Their examples:** agent that autonomously negotiates with suppliers · voice system for dynamically
personalised products · continuously-running AI research team · unstructured company data turned into
interactive simulations · autonomous service acting on behalf of customers.

**Where it scores well**

- *Originality (10)* and *Creativity (8)* — this track exists to reward exactly this. Best shot at 9–10.
- *Technical Difficulty (8)* — agentic, multimodal and autonomous systems are what the rubric names.
- *Differentiation (7)* — few or no incumbents to be compared against.

**Where it bleeds points**

- *Feasibility & Viability (8)* — **the killer.** The rubric wants cost, data access, **regulatory
  concerns** and adoption path. "An agent that autonomously negotiates with suppliers" invites exactly
  the questions you cannot answer: who is liable, what stops it agreeing to a bad price, which business
  would let it near a real supplier?
- *Impact & Value Proposition (9)* — there is **no baseline to measure against**. A new capability has no
  "hours today", so semi-quantifying the value is genuinely hard. That's 9 points at risk.
- *Functionality (10)* — the single biggest line item, and the hardest to earn here. Ambitious new
  capabilities are the projects that end up faked or hardcoded in the demo, which caps you at 5–6.
- *Use of Data/Models (6)* — no ground truth means no clean evaluation.

**The arithmetic:** Track 2 might buy you +5 to +8 across the Innovation block, while putting ~17 points
(Feasibility 8 + Impact 9) under strain and raising real execution risk on the 10-point Functionality
line. **Net negative unless somebody on the team already has a genuinely novel mechanism they can build.**

**Verdict:** the highest-ceiling, highest-variance track. Only take it if you can name, today, the
specific thing that was impossible before — *and* name who would pay for it and roughly how much.

## Track 3 — Solve a Business Problem

**Official:** start from a meaningful business problem, not from a technology. Operational, financial,
strategic, technical, customer-facing or industry-specific. Explicitly: *"you do not need to begin with
an existing capability or a particular AI technology. Start with the problem."*

**Their examples:** food/inventory waste · fraud and unusual transactions · cash-flow understanding for
small business · employee scheduling conflicts · supply-chain risk · navigating complex regulation ·
matching businesses with suppliers · customer churn · accessibility of business services.

**Where it scores well**

- *Problem Significance (8)* — the track is built around it; a sharp, well-evidenced problem with a named
  user is the whole brief.
- *Differentiation (7)* — niche problems have niche competitors nobody has heard of, so "here's what
  exists and why we're different" is much easier to win than against Intercom.
- *Originality (10)* — better than Track 1 by default, because you're not starting from a product category.
- Matches the sponsor's **"go where nobody is looking"** advice more directly than any other track.

**Where it bleeds points**

- The framing burden is entirely on you. Nothing about the track proves the problem matters — you have
  to do that work, and *Problem Significance* gives 0–4 for "unclear who actually has this problem."
- It's the catch-all. Every team that can't decide will land here, so expect the most crowded field for
  its $100.
- *Impact (9)* is harder than Track 1 unless the problem already has an hours-and-dollars shape.

**Verdict:** the best balance, and the best fit for the sponsor's advice — **provided you bring a
specific industry and a specific person with the problem.** Without that it is the weakest track,
because "solve a business problem" with a generic audience is how you score 5–6 across the whole
Business Value block.

## Special Track — Built With ElevenLabs

**Official:** open to projects from any of the three main tracks. ElevenLabs must **contribute to core
functionality, rather than simply being added as an extra feature.** You must also be in one of 1–3.

**Their examples:** real-time conversational voice agent · spoken sales/support agent · multilingual
voice interface · fully voice-driven workflow · interactive training/onboarding · personalised audio
at scale.

**The case for entering**

- Separate prize, separate judging, **much smaller field** — only teams where voice is genuinely central.
- Costs one extra line in the Devpost description if voice is already in the build.
- Everyone already has a free Creator-tier month, so there's no procurement friction.
- It maps onto real business pain in **phone-native industries**: clinics and dental practices, trades
  and dispatch, logistics, recruitment screening, debt collection, hospitality bookings, aged care,
  frontline multilingual service. These are places where the work *is* a phone call, so replacing it
  with a voice agent has an obvious hours-and-dollars baseline.

**The case against**

- *"Rather than simply being added as an extra feature"* is an explicit anti-bolt-on rule. Wrapping your
  output in TTS at 11pm Sunday will not win it and may read as padding.
- Real-time voice adds latency, interruption handling and error-recovery problems that eat hours you
  need for the 10-point Functionality line.

**Verdict:** **take it if and only if the process you picked is already a phone call or a spoken
interaction.** In that case it is close to free points. If your project is document- or dashboard-shaped,
skip it and spend the hours on the demo.

## Side-by-side, by rubric block

| Rubric block | Pts | Track 1 | Track 2 | Track 3 |
| --- | --- | --- | --- | --- |
| Functionality & Execution | 10 | **Strong** — narrow scope finishes | **Weak** — ambition gets faked | Good |
| Technical Difficulty | 8 | Risk of "API wrapper" | **Strong** | Depends on problem |
| Code Quality | 6 | Neutral — ours to win | Neutral | Neutral |
| Use of Data / Models | 6 | **Strong** — real baseline to evaluate | **Weak** — no ground truth | Good |
| Originality | 10 | **Weak** — their examples are products | **Strong** | Good |
| Creativity | 8 | Moderate | **Strong** | Moderate |
| Differentiation | 7 | **Weak** — famous competitors | Strong | **Strong** — obscure competitors |
| Problem Significance | 8 | **Strong** — pain pre-validated | Must be argued | **Strong** if industry is specific |
| Feasibility & Viability | 8 | **Strong** | **Weak** — liability, trust | Good |
| Impact & Value | 9 | **Strong** — baseline exists | **Weak** — no baseline | Good |

The execution-and-business half of the rubric (Functionality 10 + Data 6 + Feasibility 8 + Impact 9 =
**33 points**) is where Track 1 discipline wins, and it outweighs the Originality + Creativity gap
(18 points) that Track 2 buys. **In a 48-hour build, execution risk dominates.**

## What most teams will build — avoid this list

High confidence these get submitted many times over, and all sit in the rubric's "direct clone" band:

- RAG chatbot over a company's documents
- Invoice / receipt / contract extraction
- Customer support agent
- Meeting notes → CRM updates
- Resume screening
- "AI dashboard that explains your data"

If our idea is on this list, we need a very specific reason it isn't the same thing.

## Recommendation

1. **Build in Track 1's style — narrow, existing, tedious, measurable.** It protects the 33 points that
   are hardest to recover and matches how the sponsor thinks.
2. **Pick the problem from an industry someone on the team actually knows.** The founder's first
   instruction was "pick an industry you know first, then the technology." A family business, a
   part-time job, an internship, a club you administer — that's where the unglamorous processes are that
   nobody else here will think of.
3. **Bias toward Eleno's own verticals when there's a tie**: financial services and non-bank lending,
   professional services, real estate and auction houses, logistics, creative industries. The sponsor
   judge already knows the pain is real and expensive there.
4. **Avoid Track 2** unless someone can state today what was impossible before, who pays, and roughly
   how much.
5. **Enter the ElevenLabs track only if the process is a phone call.** Otherwise skip it.
6. **Declare the track label on Monday**, choosing whichever framing makes the finished project look
   sharpest. Decide the problem now; decide the label last.
7. Whatever we pick, we must be able to finish this sentence with real numbers:
   *"This task costs $X today; with our solution it costs $Y."*
