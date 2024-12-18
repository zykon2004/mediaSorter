from pathlib import Path

from mdsort.formatter import format_series_title_and_file_name
from mdsort.media_file import (
    is_downloaded_media_directory,
    is_downloaded_media_file,
    is_media_file,
)
from mdsort.parent_directory import ParentDirectory


class Sorter:
    def __init__(
        self,
        series_parent_directories: list[ParentDirectory],
        downloads_directory: Path,
        movies_directory: Path | None,
    ):
        self.downloads_directory = downloads_directory
        self.movies_directory = movies_directory
        self.series_parent_directories = series_parent_directories
        self.media_files: list[Path] = [
            file
            for file in self.downloads_directory.iterdir()
            if is_downloaded_media_file(file)
        ]
        self.media_directories: list[Path] = [
            directory
            for directory in self.downloads_directory.iterdir()
            if is_downloaded_media_directory(directory)
        ]
        self.assigned_files: list[Path] = []
        self.assigned_directories: list[Path] = []

    def assign_all_media_to_parents(self):
        for parent_directory in self.series_parent_directories:
            self.assign_files_to_parents(parent_directory)
            self.assign_directories_to_parents(parent_directory)

    def assign_files_to_parents(self, parent_directory: ParentDirectory) -> None:
        for file in self.media_files:
            if format_series_title_and_file_name(file.name).startswith(
                parent_directory.comparable_name
            ):
                parent_directory.newly_assigned_files.append(file)
                self.assigned_files.append(file)

    def assign_directories_to_parents(self, parent_directory: ParentDirectory) -> None:
        for directory in self.media_directories:
            if format_series_title_and_file_name(directory.name).startswith(
                parent_directory.comparable_name
            ):
                for file in directory.iterdir():
                    if is_media_file(file.name):
                        parent_directory.newly_assigned_files.append(file)
                self.assigned_directories.append(directory)

    def is_all_downloaded_media_assigned(self) -> bool:
        return (
            len(self.unassigned_media_files) == 0
            and len(self.unassigned_media_directories) == 0
        )

    @property
    def unassigned_media_directories(self) -> set[Path]:
        return set(self.media_directories) - set(self.assigned_directories)

    @property
    def unassigned_media_files(self) -> set[Path]:
        return set(self.media_files) - set(self.assigned_files)
