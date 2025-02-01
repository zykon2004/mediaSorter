import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from consts import A_MOVIE_DIRECTORY, MOVIES_DIRECTORY
from logger import setup_logger
from mdsort.parent_directory import ParentDirectory, find_parent_series_directories

from .consts import (
    DOWNLOADED_APP_DIRECTORY,
    DOWNLOADED_MEDIA_DIRECTORY,
    DOWNLOADED_MEDIA_FILE,
    MEDIA_SUFFIX,
    PARENT_IDENTIFIER,
    PARENT_SERIES_DIRECTORY_STR_1,
    PARENT_SERIES_DIRECTORY_STR_2,
    PERSONAL_MEDIA_DIRECTORY,
    SERIES_DIRECTORY,
)


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

    # Counts as a series directory
    mandalorian_directory = _downloads_directory / DOWNLOADED_MEDIA_DIRECTORY
    Path.mkdir(mandalorian_directory, exist_ok=True)
    Path.touch(mandalorian_directory / f"{DOWNLOADED_MEDIA_DIRECTORY}{MEDIA_SUFFIX}")
    Path.touch(mandalorian_directory / "readme.txt")

    # Does not count as a media directory
    Path.mkdir(_downloads_directory / DOWNLOADED_APP_DIRECTORY, exist_ok=True)

    # Does not count as a media directory
    wedding_videos_directory = Path(_downloads_directory / PERSONAL_MEDIA_DIRECTORY)
    Path.mkdir(wedding_videos_directory, exist_ok=True)
    Path.touch(wedding_videos_directory / f"1{MEDIA_SUFFIX}")

    # Counts as a movie directory
    a_movie_directory = Path(_downloads_directory) / A_MOVIE_DIRECTORY
    Path.mkdir(a_movie_directory, exist_ok=True)
    Path.touch(a_movie_directory / f"{A_MOVIE_DIRECTORY}{MEDIA_SUFFIX}")
    Path.touch(a_movie_directory / "readme.txt")

    # Counts as a movie file
    Path.touch(_downloads_directory / DOWNLOADED_MEDIA_FILE)

    yield _downloads_directory
    shutil.rmtree(_downloads_directory)


@pytest.fixture(scope="session")
def series_parent_directories(
    series_root_directory: Path,
) -> list[ParentDirectory]:
    return find_parent_series_directories(series_root_directory)


@pytest.fixture(scope="session")
def movies_directory() -> Generator:
    _movies_directory = Path(tempfile.mkdtemp()) / MOVIES_DIRECTORY
    Path.mkdir(_movies_directory)
    yield _movies_directory
    shutil.rmtree(_movies_directory)


@pytest.fixture(scope="session")
def logger() -> None:
    setup_logger()
