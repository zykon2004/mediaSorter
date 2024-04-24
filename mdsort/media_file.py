from pathlib import Path

import settings


def is_downloaded_media_file(file: Path) -> bool:
    return is_media_file(file.name) and is_downloaded(file.name)


def is_downloaded(filename: str) -> bool:
    return any(
        (indicator in filename for indicator in settings.DOWNLOADED_MEDIA_INDICATORS)
    )


def is_media_file(filename: str) -> bool:
    return Path(filename).suffix in settings.MEDIA_FILES_SUFFIXES


def is_downloaded_media_directory(directory: Path) -> bool:
    return is_downloaded(directory.name) and any(
        is_media_file(_file.name) for _file in directory.iterdir() if _file.is_file()
    )
