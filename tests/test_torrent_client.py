import platform
from contextlib import nullcontext
from typing import ContextManager

import pytest

import settings
import torrent_client


@pytest.mark.parametrize(
    argnames=["process_name", "context"],
    argvalues=[
        pytest.param(
            settings.TORRENT_CLIENT,
            nullcontext(),
            id="Actual torrent client isn't running",
        ),
        pytest.param(None, nullcontext(), id="Default torrent client"),
        pytest.param(
            "zsh",
            pytest.raises(torrent_client.TorrentClientIsRunningException),
            marks=pytest.mark.skipif(
                platform.system() not in ("Linux", "Darwin"),
                reason="Not linux or MacOS",
            ),
            id="zsh process is running",
        ),
    ],
)
def test_is_torrent_process_running(process_name: str, context: ContextManager):
    with context:
        torrent_client.is_running(process_name)
