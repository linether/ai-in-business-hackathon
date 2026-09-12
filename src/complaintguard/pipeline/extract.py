"""Layer 3 — structured extraction.

**Owner: @Genicayyy** (claimed on BOARD.md, 09-12 21:18). The LLM extractor is
hers to write; this file exists so the rest of the pipeline runs end to end from
the first hour rather than waiting for it.

Two implementations behind one interface:

- ``LabelledExtractor`` reads the extraction that already sits in the scenario
  file. It needs no API key and no network, so the app is demoable immediately
  and the deterministic layers downstream can be developed and tested on real
  shapes. **It is not a model — it cannot be evaluated, because it is reading
  the answers.**
- ``LLMExtractor`` is the real one. Stub for now.

Swap by passing a different extractor to ``pipeline.analyse``; nothing else in
the codebase needs to change.
"""

from __future__ import annotations

from typing import Optional, Protocol

from ..models import Case, Extraction


class Extractor(Protocol):
    """Anything that can turn a contact's transcript into structured claims."""

    name: str

    def extract(self, case: Case, contact_seq: int) -> Optional[Extraction]:
        ...


class LabelledExtractor:
    """Reads the ground-truth extraction already loaded onto the case.

    Useful for building and demoing the rest of the system. Useless for
    measuring anything — see the docstring at the top of this file.
    """

    name = "labelled-stub"

    def extract(self, case: Case, contact_seq: int) -> Optional[Extraction]:
        contact = next((c for c in case.contacts if c.seq == contact_seq), None)
        return contact.extraction if contact else None


class LLMExtractor:
    """The real extractor. @Genicayyy owns this.

    Contract it has to satisfy — the rest of the pipeline depends on all four:

    1. Return an ``Extraction`` for the contact: needs, promises, actions.
    2. **Every claim carries at least one ``Evidence`` with a verbatim ``quote``
       and the ``utterance_index`` it came from.** The citation check (3b) and
       the whole evaluation both key off that index; a claim without one cannot
       be verified and will be marked UNCERTAIN.
    3. Never paraphrase inside ``quote``. Copy the words exactly as transcribed.
    4. Prefer omitting a claim over inventing one. A missed promise costs recall;
       a fabricated promise blames a person.

    Suggested shape: ask the model for strict JSON keyed by utterance index, then
    validate against the models here before returning. See
    docs/spec.md §4 and docs/architecture-upgrade.md.
    """

    name = "llm"

    def __init__(self, model: str = "claude-sonnet-5") -> None:
        self.model = model

    def extract(self, case: Case, contact_seq: int) -> Optional[Extraction]:
        raise NotImplementedError(
            "LLMExtractor is not implemented yet — @Genicayyy owns layer 3. "
            "Run with LabelledExtractor until it lands."
        )
