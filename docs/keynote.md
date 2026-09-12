# Opening night — keynote + logistics (10 Sep)

From the transcript of opening night. The keynote speaker is the **founder of Eleno**, the sponsor —
treat his "how to win" section as a judge telling us the answer, because it effectively is.

## ⚠️ Hard rules that weren't on the wiki

- **Git history is submitted and inspected.** *"You will have to submit your GitHub and your GitHub
  history. If I see teams committing [early], or their first commit is like the entire codebase, we
  know that you're cheating."*
- **No coding before Sat 12:00pm.** Planning, brainstorming and research before then were explicitly
  encouraged — *"from now to Saturday, start planning"* — but no application code.
- **Our position:** this repo's pre-Saturday commits are planning docs only (brief, plan, rubric,
  decisions). No application code existed before Sat 12pm. That's exactly what they asked for, and an
  incremental commit history is evidence *for* us, not against. Keep it that way: docs commits stay
  docs-only, and every code commit lands after Sat 12pm.
- **Team registration is a soft deadline.** *"Please register before the hackathon starts. It's not the
  end of the world if you don't register, but it's very important that we get that information at the
  very end."* Still do it now: https://forms.gle/tUDRz7TwGGXUzKFZ9
- **Finals venue: Latham Theatre.** Finalists must attend **in person** to receive the prize.
- **Discord + email are the official comms channels.** The wiki link lives in `#announcements`, pinned.
- Production-ready accessible site = *"major bonus points"*.
- Prize detail: all participants get 1 month ElevenLabs Creator; **overall winner also gets 3 months
  Pro**; best ElevenLabs project takes the special track prize. The special track requires you to also
  be in one of tracks 1–3.

## How the sponsor says teams win

His stated losing pattern: *"focusing only on the technology"* — hundreds of ideas, pick one, never
stress-test it against data outside the room, start vibe-coding immediately.

His winning pattern:

1. **Pick an industry you know first, then the technology.** Not the other way round.
2. **Pick a problem you can measure**, where someone somewhere will actually pay.
3. **Go for the tedious work.** *"Never fear what it's worth — name the dollar amount."*
4. **Validate against real market data before building the rest of the solution.**
5. **Shrink the job down.** Prove one narrow use case rather than promising a grand system.
6. **Go where nobody is looking.**

His three tests before pursuing any idea — we should run these on our idea before writing code:

- Can you **describe the output** precisely?
- Can you **name the dollar value** — hours × rate × volume per week? *"If you can't ascribe nearly a
  perfect economic unit to how much money or time you're going to save a business, I don't think it's
  worth pursuing."*
- **Half-build it** and get market validation before doing the hard engineering.

And the closing line, which is the single most actionable thing said all night:

> *"If you can turn up to the judging panel and say, 'This is what we think this task costs today, and
> this is what it will cost with our solution,' with a straight face, I think that's how you've got the
> best chance to win."*

**That sentence belongs in our pitch, with real numbers in it.**

## Weighting, in his own words

*"This hackathon will partially be judged by how much it would impact a business economically and
financially, as opposed to just the strength of the solution or the codebase... but I promised Nathan
that the vast majority of the ranking points will still be on the codebase and the technology, and a
little bit of it will be about the business application."*

Consistent with the rubric: 30 technical + 25 innovation + **25 business value** out of 80.
Technology still carries it — the business case is what breaks the tie.

## His framing of the opportunity

- He asked the room what share of business AI solutions have already been built. His answer: **~5%**.
- Big tech incumbents skip SMEs and mid-market as *"too small to serve"* — yet two private-credit firms
  with $1–2bn AUM each spent **over $250k** on operations work.
- Advantage for students: you may understand two or three of a business's processes better than people
  twice your age, and can automate them.

## His case studies — the shape of a winning project

Useful as templates, and as a signal of what the sponsor finds impressive.

| Client | What they built | Result |
| --- | --- | --- |
| **Private credit** | Ingest ~150pp valuation/QS reports + a 407-variable Excel feasibility model + borrower PDFs; extract hundreds of variables; downstream loan-doc generation | Extraction **52 min → 30 sec**. Term sheet/memo drafting **days → ~2 hrs of review**. Platform has since processed **$1bn+** in loans |
| **Auction house** | Sales-pattern agent across 80–90k clients: interests, past purchases, and crucially **bids they lost** | Found a client who'd spent $1,200 but had lost a $60k artwork → auto-outreach → **they spent $80,000**. Prep **25 hrs → 2–3 hrs**; outreach **150–200 → ~1,000**. Across 5 auctions: **~$900k of sales for ~$550 of compute** |
| **Commercial real estate** | Client asked them to automate *all* inquiry management; they said no and did **invoice extraction** first | Targeted a staffer spending **3.5 days/week** reading invoices. **9-month payback**, measurable — which won them a far longer contract |
| **Invoice reconciliation** | OCR pipeline extracting fields, escalating to a human **only on anomalies** | Manual review **100% → 8%**. Staffer went from **104 hrs/month** on invoices to sales support |

**One architecture note worth stealing:** for the money-critical numbers he used *"automation pipelines
to process numbers, as opposed to agents that could maybe make mistakes."* Deterministic where money is
at stake, LLM where judgement is needed — and being able to explain that split is exactly the
"understands the *why* behind their architecture choices" language in the Technical Difficulty rubric.
