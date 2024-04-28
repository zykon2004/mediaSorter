import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest

import media_file
import settings


@pytest.mark.parametrize(
    argnames=["filename", "expected_result"],
    argvalues=[
        pytest.param(
            "The.Mandalorian.S02E02.Chapter.10.1080p.DSNP.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX.mkv",
            True,
            id="A file ending with .mkv and contains 1080p",
        ),
        pytest.param(
            "The.Mandalorian.S02E02.Chapter.10.1080p.DSNP.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX",
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

    media_suffix = settings.MEDIA_FILES_SUFFIXES[0]
    media_indicator = settings.DOWNLOADED_MEDIA_INDICATORS[0]

    mandalorian_file_name = f"The.Mandalorian.S02E02.Chapter.10.{media_indicator}.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX"
    mandalorian_directory = _downloads_directory / mandalorian_file_name
    Path.mkdir(mandalorian_directory, exist_ok=True)
    Path.touch(mandalorian_directory / f"{mandalorian_file_name}{media_suffix}")
    Path.touch(mandalorian_directory / "readme.txt")

    Path.mkdir(_downloads_directory / "Photoshop CS2", exist_ok=True)

    wedding_videos_directory = Path(_downloads_directory / "Wedding Videos")
    Path.mkdir(wedding_videos_directory, exist_ok=True)
    Path.touch(wedding_videos_directory / f"1{media_suffix}")

    Path.touch(
        _downloads_directory
        / f"S.W.A.T.2017.S07E10.{media_indicator}.HDTV.x265-MiNX[TGx].{media_suffix}"
    )
    yield _downloads_directory
    shutil.rmtree(_downloads_directory)


def test_find_downloaded_file_in_directory(downloads_directory: Path) -> None:
    assert (
        len(
            [
                media_file.is_downloaded_media_directory(directory)
                for directory in downloads_directory.iterdir()
                if directory.is_dir()
            ]
        )
        == 1
    )
