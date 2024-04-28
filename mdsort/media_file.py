from pathlib import Path

import settings


def is_downloaded_media_file(filename: str) -> bool:
    return is_media_file(filename) and is_downloaded(filename)


def is_downloaded(filename: str) -> bool:
    return any(
        (indicator in filename for indicator in settings.DOWNLOADED_MEDIA_INDICATORS)
    )


def is_media_file(filename: str) -> bool:
    return Path(filename).suffix in settings.MEDIA_FILES_SUFFIXES


def is_downloaded_media_directory(directory: Path):
    return None
