"""Keep the test suite offline.

`live.py` calls `load_dotenv()` so that running uvicorn directly picks up a key
from `.env` — which also means pytest picks it up, and the moment the live room
learned to speak, the offline suite started calling ElevenLabs and spending
credits on every run. It is called an offline suite in three docstrings; this
makes that true rather than aspirational.

Voice is switched off for every test. The tests that care about speech assert on
the *decision* to speak, which is what we wrote, rather than on ElevenLabs, which
we did not.
"""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True, scope="session")
def _no_network(request):
    import os

    os.environ["LIVE_VOICE"] = "off"
    yield
