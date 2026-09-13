"""Retrieval over Meridian Mobile's support policy.

Twelve short documents, scored with BM25, in memory, in plain Python.

**No vector store, and that is a decision rather than a shortcut.** Embeddings buy
semantic recall, which matters when the corpus is large enough that a question and
its answer share no words. Over twelve documents written in the same register as
the questions — "callback", "refund", "add-on", "ombudsman" — lexical matching
finds the right one, and it does so with no index to build, no service to call,
no dimension to get wrong and no extra failure mode on a live call. When the
corpus grows past a few hundred documents the argument flips and this should be
replaced; it is one function behind one interface, so that is a class, not a
refactor.

What retrieval is *for* here is worth being precise about. It is not to make the
demo agent sound knowledgeable. It is so there is a written rule the agent can be
measured against — the supervisor's contradiction signal only means something if
"what the policy says" exists somewhere outside the model's head.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

POLICY_DIR = Path(__file__).resolve().parents[2] / "data" / "policy"

# Words that carry no discriminating power over a corpus of support policies.
STOP = frozenset("""
a an and are as at be been before by can do does for from had has have if in into is it its may
must no not of on or our so than that the their them then there these they this to under until was
were what when where which who will with within would you your
""".split())

_TOKEN = re.compile(r"[a-z][a-z'-]*")

# BM25 constants. k1 controls how fast term frequency saturates, b how much long
# documents are penalised. These are the standard defaults and there is no tuning
# set to tune them against, so they stay at the defaults and we say so.
K1 = 1.5
B = 0.75


def tokenise(text: str) -> List[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in STOP and len(t) > 1]


class Chunk:
    """One policy document, plus the counts BM25 needs."""

    def __init__(self, path: Path, title: str, ref: str, body: str, also: str = "") -> None:
        self.path = path
        self.slug = path.stem
        self.title = title
        self.ref = ref
        self.body = body
        self.also = also
        # The alias line is indexed but never shown to the model or the visitor.
        # It exists because the policies are written in staff register and people
        # ring up in their own words: the document says "dropouts", the customer
        # says "it keeps cutting out". A lexical retriever can only bridge that if
        # the bridge is written down, so each policy declares its own synonyms
        # rather than us hoping the stemmer saves us.
        self.tokens = tokenise(" ".join([title, also, body]))
        self.tf = Counter(self.tokens)
        self.length = len(self.tokens) or 1

    @property
    def label(self) -> str:
        return "{} ({})".format(self.title, self.ref) if self.ref else self.title

    def __repr__(self) -> str:  # pragma: no cover - debugging only
        return "<Chunk {} {}>".format(self.slug, self.ref)


def _parse(path: Path) -> Optional[Chunk]:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    if not lines or not lines[0].startswith("# "):
        return None
    title = lines[0][2:].strip()
    ref = ""
    also = ""
    body_start = 1
    for i, line in enumerate(lines[1:6], start=1):
        low = line.lower()
        if low.startswith("ref:"):
            ref = line.split(":", 1)[1].strip()
            body_start = max(body_start, i + 1)
        elif low.startswith("also:"):
            also = line.split(":", 1)[1].strip()
            body_start = max(body_start, i + 1)
    body = "\n".join(lines[body_start:]).strip()
    return Chunk(path, title, ref, body, also)


class Corpus:
    """The policy folder, loaded once."""

    def __init__(self, directory: Path = POLICY_DIR) -> None:
        self.directory = directory
        self.chunks: List[Chunk] = []
        self.df: Counter = Counter()
        self.avg_len = 1.0
        self.load()

    def load(self) -> None:
        self.chunks = []
        if not self.directory.is_dir():
            return
        for path in sorted(self.directory.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            chunk = _parse(path)
            if chunk is not None:
                self.chunks.append(chunk)

        self.df = Counter()
        for chunk in self.chunks:
            for term in set(chunk.tokens):
                self.df[term] += 1
        total = sum(c.length for c in self.chunks)
        self.avg_len = (total / len(self.chunks)) if self.chunks else 1.0

    def _idf(self, term: str) -> float:
        n = len(self.chunks)
        df = self.df.get(term, 0)
        if df == 0:
            return 0.0
        # The +0.5/+0.5 form, floored at zero so a term in every document cannot
        # drag a score negative.
        return max(0.0, math.log(1 + (n - df + 0.5) / (df + 0.5)))

    def score(self, query_tokens: List[str], chunk: Chunk) -> float:
        total = 0.0
        for term in query_tokens:
            tf = chunk.tf.get(term, 0)
            if not tf:
                continue
            idf = self._idf(term)
            norm = tf * (K1 + 1) / (tf + K1 * (1 - B + B * chunk.length / self.avg_len))
            total += idf * norm
        return total

    def search(self, query: str, k: int = 2, floor: float = 0.6) -> List[Chunk]:
        """Top-k policies for a question, or nothing if nothing is relevant.

        The floor matters more than the ranking. Returning the least-irrelevant
        document for an off-topic question is how a retrieval layer teaches a
        model to say something confidently wrong, so below the floor this returns
        an empty list and the agent is told there is no policy on the point.
        """
        tokens = tokenise(query)
        if not tokens or not self.chunks:
            return []
        scored = [(self.score(tokens, c), c) for c in self.chunks]
        scored.sort(key=lambda pair: (-pair[0], pair[1].slug))
        return [c for s, c in scored[:k] if s >= floor]

    def by_slug(self, slug: str) -> Optional[Chunk]:
        return next((c for c in self.chunks if c.slug == slug), None)


_corpus: Optional[Corpus] = None


def corpus() -> Corpus:
    global _corpus
    if _corpus is None:
        _corpus = Corpus()
    return _corpus


def search(query: str, k: int = 2) -> List[Chunk]:
    return corpus().search(query, k=k)


def as_prompt(chunks: List[Chunk]) -> str:
    """Render retrieved policy for the agent's system prompt."""
    if not chunks:
        return "No Meridian Mobile policy covers this point. Say so rather than inventing a rule."
    return "\n\n".join(
        "--- POLICY {} — {} ---\n{}".format(c.ref or "?", c.title, c.body) for c in chunks
    )
