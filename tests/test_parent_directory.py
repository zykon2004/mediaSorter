import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest

import settings
from mdsort.parent_directory import find_parent_series_directories, ParentDirectory

PARENT_IDENTIFIER = settings.PARENT_IDENTIFIER
PARENT_SERIES_DIRECTORY_1 = "Mandalorian 2018"
PARENT_SERIES_DIRECTORY_2 = "Avatar: The Last Airbender tt9018736"
SERIES_DIRECTORY = "Catch 22"


@pytest.fixture(scope="module")
def temp_directory() -> Path:
    return Path(tempfile.mkdtemp())


@pytest.fixture(scope="module")
def series_root_directory(temp_directory: Path) -> Generator:
    _series_root_directory = temp_directory
    for parent_series_directory in (
        PARENT_SERIES_DIRECTORY_1,
        PARENT_SERIES_DIRECTORY_2,
    ):
        _directory = _series_root_directory / parent_series_directory
        Path.mkdir(_directory, exist_ok=True)
        Path.touch(_directory / PARENT_IDENTIFIER)

    _non_parent_series_directory = _series_root_directory / SERIES_DIRECTORY
    Path.mkdir(_non_parent_series_directory, exist_ok=True)

    yield _series_root_directory
    shutil.rmtree(_series_root_directory)


def test_find_all_parent_series_directories(
    series_root_directory: Path,
    parent_directory_1: ParentDirectory,
    parent_directory_2: ParentDirectory,
) -> None:
    assert find_parent_series_directories(series_root_directory) == [
        parent_directory_1,
        parent_directory_2,
    ]


@pytest.fixture(scope="module")
def parent_directory_1(temp_directory: Path) -> ParentDirectory:
    return ParentDirectory(
        path=temp_directory / Path(PARENT_SERIES_DIRECTORY_1),
        newly_assigned_files=[],
    )


@pytest.fixture(scope="module")
def parent_directory_2(temp_directory: Path) -> ParentDirectory:
    return ParentDirectory(
        path=temp_directory / Path(PARENT_SERIES_DIRECTORY_2),
        newly_assigned_files=[],
    )


def test_parent_directory_comparable_name(parent_directory_2) -> None:
    assert parent_directory_2.comparable_name == "avatar.the.last.airbender"


def test_parent_directory_assigned_files_proper_path(parent_directory_2) -> None:
    newly_assigned_files = [Path("Avatar The Last Airbender s01e02.mkv")]
    assert (
        parent_directory_2.resolve_new_file_path(newly_assigned_files[0])
        == parent_directory_2.path / "Avatar: The Last Airbender - 01x02.mkv"
    )
