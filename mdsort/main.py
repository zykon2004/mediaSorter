#!/usr/bin/env -S uv run
import logging
from pathlib import Path

import logger
import settings

from mdsort.parent_directory import find_parent_series_directories
from mdsort.sorter import Sorter


def driver() -> None:
    logger.setup_logger()
    logging.info("#### MediaSorter Started ####")
    sorter = Sorter(
        series_parent_directories=find_parent_series_directories(
            Path(settings.TV_SHOWS_DIRECTORY)
        ),
        downloads_directory=Path(settings.DOWNLOADS_DIRECTORY),
        movies_directory=Path(settings.MOVIES_DIRECTORY),
    )
    sorter.sort()
    logging.info("#### MediaSorter Ended ####")


if __name__ == "__main__":
    driver()
