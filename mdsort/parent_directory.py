from pathlib import Path

import settings


def find_parent_series_directories(series_root_directory: Path) -> set[str]:
    return {
        directory.name
        for directory in series_root_directory.iterdir()
        if Path(directory / settings.PARENT_IDENTIFIER).exists()
    }
