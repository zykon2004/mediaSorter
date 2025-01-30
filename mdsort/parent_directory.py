from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

import settings

from mdsort.formatter import (
    format_series_filename_before_rename,
    format_series_title_and_file_name,
)


@dataclass
class ParentDirectory:
    path: Path
    newly_assigned_files: list[Path] = field(default_factory=list)

    @cached_property
    def comparable_name(self):
        return format_series_title_and_file_name(self.path.name)

    @staticmethod
    def is_parent_directory(directory: Path) -> bool:
        return Path(directory / settings.PARENT_IDENTIFIER).exists()

    def resolve_new_file_path(self, assigned_file: Path):
        return self.path / format_series_filename_before_rename(
            assigned_file.name, self.path.name
        )


def find_parent_series_directories(
    series_root_directory: Path,
) -> list[ParentDirectory]:
    return [
        ParentDirectory(path=directory)
        for directory in series_root_directory.iterdir()
        if ParentDirectory.is_parent_directory(directory)
    ]
