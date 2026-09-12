"""ElevenLabs integration: text-to-speech for the corpus, Scribe for transcription.

⚠️ **Neither has run against the live API** — no key was available when these
were written. Both have a ``--dry-run`` that exercises everything except the
network call, and both refuse to spend credits on work already done.

Credit budget is the binding constraint, not correctness. The Creator tier is
121,000 credits a month; speech-to-text costs roughly 330 credits a minute, so a
single afternoon of re-transcribing the same audio while debugging would empty
it. Hence: **everything caches, and the cache is checked first.**

The evaluation set does not need audio at all — it measures extraction and
reasoning over transcripts. Generate audio only for the handful of scenarios that
appear in the demo video.
"""
