import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest

import parent_directory
import settings

PARENT_IDENTIFIER = settings.PARENT_IDENTIFIER
PARENT_SERIES_DIRECTORY_1 = "Mandalorian 2018"
PARENT_SERIES_DIRECTORY_2 = "Avatar: The Last Airbender tt9018736"
SERIES_DIRECTORY = "Catch 22"


@pytest.fixture(scope="module")
def series_root_directory() -> Generator:
    _series_root_directory = Path(tempfile.mkdtemp())
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


def test_find_all_parent_series_directories(series_root_directory: Path) -> None:
    assert parent_directory.find_parent_series_directories(series_root_directory) == {
        PARENT_SERIES_DIRECTORY_1,
        PARENT_SERIES_DIRECTORY_2,
    }


@pytest.fixture(scope="module")
def parent_directory_2() -> parent_directory.ParentDirectory:
    return parent_directory.ParentDirectory(
        path=Path(PARENT_SERIES_DIRECTORY_2),
        newly_assigned_files=[Path("Avatar The Last Airbender s01e02.mkv")],
    )


def test_parent_directory_comparable_name(parent_directory_2) -> None:
    assert parent_directory_2.comparable_name == "avatar.the.last.airbender"


def test_parent_directory_assigned_files_proper_path(parent_directory_2) -> None:
    assert (
        parent_directory_2.resolve_new_file_path(
            parent_directory_2.newly_assigned_files[0]
        )
        == parent_directory_2.path / "Avatar: The Last Airbender - 01x02.mkv"
    )
