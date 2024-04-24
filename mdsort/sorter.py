from pathlib import Path

import media_file
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
        self.media_files: list[Path] = [
            file
            for file in self.downloads_directory.iterdir()
            if media_file.is_downloaded_media_file(file)
        ]
        self.media_directories: list[Path] = [
            directory
            for directory in self.downloads_directory.iterdir()
            if media_file.is_downloaded_media_directory(directory)
        ]
