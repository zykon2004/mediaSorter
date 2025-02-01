#!/usr/bin/env -S uv run
import logging
from pathlib import Path

from mdsort.parent_directory import find_parent_series_directories
from mdsort.sorter import Sorter

from . import logger, settings


def driver() -> None:
    logger.setup_logger()
    logging.info("### MediaSorter Started ###")
    tv_shows_directory, downloads_directory, movies_directory = validate_directories()
    sorter = Sorter(
        series_parent_directories=find_parent_series_directories(
            Path(tv_shows_directory)
        ),
        downloads_directory=Path(downloads_directory),
        movies_directory=Path(movies_directory),
    )
    sorter.sort()
    logging.info("#### MediaSorter Ended ####")


def validate_directories() -> tuple[Path, Path, Path]:
    # for mypy
    assert isinstance(settings.TV_SHOWS_DIRECTORY, str)
    assert isinstance(settings.DOWNLOADS_DIRECTORY, str)
    assert isinstance(settings.MOVIES_DIRECTORY, str)

    tv_shows = Path(settings.TV_SHOWS_DIRECTORY)
    downloads = Path(settings.DOWNLOADS_DIRECTORY)
    movies = Path(settings.MOVIES_DIRECTORY)
    if all((tv_shows.is_dir(), downloads.is_dir(), movies.is_dir())):
        return tv_shows, downloads, movies
    else:
        raise ValueError(
            "One of the the supplied directories in not a directory at all!"
        )


if __name__ == "__main__":
    driver()
