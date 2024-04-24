from pathlib import Path

from parent_directory import ParentDirectory


class Sorter:
    def __init__(
        self,
        series_parent_directories: list[ParentDirectory],
        downloads_directory: Path,
        movies_directory: Path,
    ):
        self.downloads_directory = downloads_directory
        self.movies_directory = movies_directory
        self.series_parent_directories = series_parent_directories
