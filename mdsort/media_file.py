from pathlib import Path

import settings


def is_media_file(filename: str) -> bool:
    return Path(filename).suffix in settings.MEDIA_FILES_SUFFIXES and any(
        (indicator in filename for indicator in settings.DOWNLOADED_MEDIA_INDICATORS)
    )
