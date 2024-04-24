import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from .consts import (
    PERSONAL_MEDIA_DIRECTORY,
    MEDIA_INDICATOR,
    SERIES_DIRECTORY,
    DOWNLOADED_MEDIA_DIRECTORY,
    MEDIA_SUFFIX,
    DOWNLOADED_APP_DIRECTORY,
    PARENT_IDENTIFIER,
    PARENT_SERIES_DIRECTORY_STR_1,
    PARENT_SERIES_DIRECTORY_STR_2,
)
from mdsort.parent_directory import ParentDirectory


@pytest.fixture(scope="session")
def temp_directory() -> Path:
    return Path(tempfile.mkdtemp())


@pytest.fixture(scope="session")
def series_root_directory(
    temp_directory: Path,
) -> Generator:
    _series_root_directory = temp_directory
    for parent_series_directory in (
        PARENT_SERIES_DIRECTORY_STR_1,
        PARENT_SERIES_DIRECTORY_STR_2,
    ):
        _directory = _series_root_directory / parent_series_directory
        Path.mkdir(_directory, exist_ok=True)
        Path.touch(_directory / PARENT_IDENTIFIER)

    _non_parent_series_directory = _series_root_directory / SERIES_DIRECTORY
    Path.mkdir(_non_parent_series_directory, exist_ok=True)

    yield _series_root_directory
    shutil.rmtree(_series_root_directory)


@pytest.fixture(scope="session")
def parent_directory_1(
    temp_directory: Path,
) -> ParentDirectory:
    return ParentDirectory(
        path=temp_directory / Path(PARENT_SERIES_DIRECTORY_STR_1),
        newly_assigned_files=[],
    )


@pytest.fixture(scope="session")
def parent_directory_2(
    temp_directory: Path,
) -> ParentDirectory:
    return ParentDirectory(
        path=temp_directory / Path(PARENT_SERIES_DIRECTORY_STR_2),
        newly_assigned_files=[],
    )


@pytest.fixture(scope="session")
def downloads_directory() -> Generator:
    _downloads_directory = Path(tempfile.mkdtemp())

    mandalorian_directory = _downloads_directory / DOWNLOADED_MEDIA_DIRECTORY
    Path.mkdir(mandalorian_directory, exist_ok=True)
    Path.touch(mandalorian_directory / f"{DOWNLOADED_MEDIA_DIRECTORY}{MEDIA_SUFFIX}")
    Path.touch(mandalorian_directory / "readme.txt")

    Path.mkdir(_downloads_directory / DOWNLOADED_APP_DIRECTORY, exist_ok=True)

    wedding_videos_directory = Path(_downloads_directory / PERSONAL_MEDIA_DIRECTORY)
    Path.mkdir(wedding_videos_directory, exist_ok=True)
    Path.touch(wedding_videos_directory / f"1{globals}")

    Path.touch(
        _downloads_directory
        / f"S.W.A.T.2017.S07E10.{MEDIA_INDICATOR}.HDTV.x265-MiNX[TGx]{MEDIA_SUFFIX}"
    )
    yield _downloads_directory
    shutil.rmtree(_downloads_directory)
