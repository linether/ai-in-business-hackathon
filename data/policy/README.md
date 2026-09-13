# Meridian Mobile — internal support policy

**Meridian Mobile is fictional and so is every rule in this folder.** The documents are written by
the team to give the demo agent at `/live` something concrete to be right or wrong about, and to
give ComplaintGuard something to check the agent against.

The timeframes are modelled on ordinary Australian telco practice and on the
[TIO](https://www.tio.com.au/) complaint-handling expectations cited in
[`docs/market-evidence.md`](../../docs/market-evidence.md), but **no real provider's policy is
reproduced here.**

One file per policy, one policy per file. The retriever in
[`src/complaintguard/knowledge.py`](../../src/complaintguard/knowledge.py) reads the whole folder at
import and scores chunks lexically — there is no index to rebuild, so adding a file is enough.

Front matter each file must carry:

    # <title>
    ref: <section number, e.g. 4.2>
    also: <customer-language synonyms, space separated>

Everything after that is the body — what the retriever scores and what the agent is shown.

The `also:` line is **indexed but never shown**, to anyone. It exists because these documents are
written in staff register and customers ring up in their own words: the policy says *dropouts*, the
customer says *it keeps cutting out*. Lexical retrieval can only cross that gap if the crossing is
written down, so each policy declares its own synonyms instead of us hoping a stemmer rescues it.
