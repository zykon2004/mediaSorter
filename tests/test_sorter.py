from pathlib import Path

import pytest

from mdsort.parent_directory import ParentDirectory
from mdsort.sorter import Sorter

from .consts import DOWNLOADED_MEDIA_DIRECTORY, DOWNLOADED_MEDIA_FILE


@pytest.fixture(scope="function")
def sorter(
    downloads_directory: Path,
    series_parent_directories: list[ParentDirectory],
    movies_directory: Path | None,
) -> Sorter:
    return Sorter(
        downloads_directory=downloads_directory,
        series_parent_directories=series_parent_directories,
        movies_directory=movies_directory,
    )


def test_sorter_init(sorter: Sorter, downloads_directory: Path):
    assert sorter.media_files == [downloads_directory / DOWNLOADED_MEDIA_FILE]
    assert sorter.media_directories == [
        downloads_directory / DOWNLOADED_MEDIA_DIRECTORY
    ]


def test_sorter_assign_media_to_parents(sorter: Sorter):
    sorter.assign_all_media_to_parents()
    assert len(sorter.series_parent_directories[0].newly_assigned_files) > 0
    assert (
        not sorter.is_all_downloaded_media_assigned()
        and len(sorter.unassigned_media_files) == 1
    )
