from pathlib import Path

import settings

from mdsort import formatter


def is_downloaded_media_file(file: Path) -> bool:
    return is_media_file(file.name) and is_downloaded(file.name)


def is_downloaded(filename: str) -> bool:
    return any(
        indicator in filename for indicator in settings.DOWNLOADED_MEDIA_INDICATORS
    )


def is_media_file(filename: str) -> bool:
    return Path(filename).suffix in settings.MEDIA_FILES_SUFFIXES


def is_downloaded_media_directory(directory: Path) -> bool:
    return (
        directory.is_dir()
        and is_downloaded(directory.name)
        and any(
            is_media_file(_file.name) for _file in directory.iterdir() if _file.is_file()
        )
    )


def is_series_file(file: Path) -> bool:
    if not is_downloaded_media_file(file):
        return False
    try:
        formatter.extract_season_and_episode_from_series_filename(file.name)
    except formatter.SeasonEpisodePatternNotFound:
        return False
    else:
        return True
