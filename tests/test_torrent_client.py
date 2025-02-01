import platform
from contextlib import AbstractContextManager, nullcontext

import pytest

# from mdsort import settings, torrent_client
from mdsort import torrent_client


@pytest.mark.parametrize(
    argnames=["process_name", "context"],
    argvalues=[
        # pytest.param(
        #     settings.TORRENT_CLIENT,
        #     nullcontext(),
        #     id="Actual torrent client isn't running",
        # ),
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
def test_is_torrent_process_running(
    process_name: str, context: AbstractContextManager
) -> None:
    with context:
        torrent_client.is_running(process_name)
