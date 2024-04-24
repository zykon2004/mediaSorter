from pathlib import Path
from typing import Optional

import pytest


from .consts import DOWNLOADED_MEDIA_FILE, DOWNLOADED_MEDIA_DIRECTORY
from parent_directory import ParentDirectory
from sorter import Sorter


@pytest.fixture(scope="session")
def sorter(
    downloads_directory: Path,
    series_parent_directories: list[ParentDirectory],
    movies_directory: Optional[Path],
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
