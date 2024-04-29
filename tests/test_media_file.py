import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest

import media_file
import settings

MEDIA_SUFFIX = settings.MEDIA_FILES_SUFFIXES[0]
MEDIA_INDICATOR = settings.DOWNLOADED_MEDIA_INDICATORS[0]
DOWNLOADED_MEDIA_DIRECTORY = f"The.Mandalorian.S02E02.Chapter.10.{MEDIA_INDICATOR}.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX"
PERSONAL_MEDIA_DIRECTORY = "Wedding Videos"
DOWNLOADED_APP_DIRECTORY = "Photoshop CS2"


@pytest.mark.parametrize(
    argnames=["filename", "expected_result"],
    argvalues=[
        pytest.param(
            f"The.Mandalorian.S02E02.Chapter.10.{MEDIA_INDICATOR}.DSNP.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX.mkv",
            True,
            id=f"A file ending with .mkv and contains {MEDIA_INDICATOR}",
        ),
        pytest.param(
            f"The.Mandalorian.S02E02.Chapter.10.{MEDIA_INDICATOR}.DSNP.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX",
            False,
            id="Contains downloaded media pattern but is not a file",
        ),
        pytest.param(
            "Our Wedding 2019.mkv",
            False,
            id="A file ending with .mkv but does not contain a downloaded media pattern",
        ),
    ],
)
def test_format_before_rename_raises_exceptions(
    filename: str, expected_result: bool
) -> None:
    assert media_file.is_downloaded_media_file(filename) == expected_result


@pytest.fixture(scope="module")
def downloads_directory() -> Generator:
    _downloads_directory = Path(tempfile.mkdtemp())

    mandalorian_directory = _downloads_directory / DOWNLOADED_MEDIA_DIRECTORY
    Path.mkdir(mandalorian_directory, exist_ok=True)
    Path.touch(mandalorian_directory / f"{DOWNLOADED_MEDIA_DIRECTORY}{MEDIA_SUFFIX}")
    Path.touch(mandalorian_directory / "readme.txt")

    Path.mkdir(_downloads_directory / DOWNLOADED_APP_DIRECTORY, exist_ok=True)

    wedding_videos_directory = Path(_downloads_directory / PERSONAL_MEDIA_DIRECTORY)
    Path.mkdir(wedding_videos_directory, exist_ok=True)
    Path.touch(wedding_videos_directory / f"1{MEDIA_SUFFIX}")

    Path.touch(
        _downloads_directory
        / f"S.W.A.T.2017.S07E10.{MEDIA_INDICATOR}.HDTV.x265-MiNX[TGx]{MEDIA_SUFFIX}"
    )
    yield _downloads_directory
    shutil.rmtree(_downloads_directory)


def test_find_downloaded_file_in_directory(downloads_directory: Path) -> None:
    assert media_file.is_downloaded_media_directory(
        downloads_directory / DOWNLOADED_MEDIA_DIRECTORY
    )


def test_downloaded_app_directory_is_not_recognized_as_downloaded_media_directory(
    downloads_directory: Path,
):
    assert not media_file.is_downloaded_media_directory(
        downloads_directory / DOWNLOADED_APP_DIRECTORY
    )


def test_personal_media_folder_is_not_recognized_as_downloaded_media(
    downloads_directory: Path,
):
    assert not media_file.is_downloaded_media_directory(
        downloads_directory / PERSONAL_MEDIA_DIRECTORY
    )
