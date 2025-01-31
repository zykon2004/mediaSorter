import logging
import shutil
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
    ) -> None:
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

    def sort(self) -> None:
        self.assign_all_media_to_parents()
        self.move_all_media_to_assigned_parents()
        self.move_unassigned_media_to_movies()
        self.cleanup_empty_directories()

    def assign_all_media_to_parents(self) -> None:
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

    def move_all_media_to_assigned_parents(self) -> None:
        for parent_directory in self.series_parent_directories:
            for file in parent_directory.newly_assigned_files:
                src = file
                dst = parent_directory.resolve_new_file_path(file)
                self.move(src, dst)

    @staticmethod
    def move(src: Path, dst: Path) -> None:
        shutil.move(src, dst)
        logging.info("Moved: %s", src)
        logging.info("To: %s", dst)

    def move_unassigned_media_to_movies(self) -> None:
        self.move_unassigned_files_to_movies()
        self.move_unassigned_directories_to_movies()

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

    def move_unassigned_files_to_movies(self) -> None:
        for file in self.unassigned_media_files:
            src = file
            dst = self.movies_directory / src
            self.move(src, dst)

    def move_unassigned_directories_to_movies(self) -> None:
        for directory in self.unassigned_media_directories:
            src = directory
            dst = self.movies_directory / src
            self.move(src, dst)

    def cleanup_empty_directories(self) -> None:
        for directory in self.assigned_directories:
            logging.info("Deleted %s", directory)
            shutil.rmtree(directory)
