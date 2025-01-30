from pathlib import Path

from mdsort.parent_directory import ParentDirectory, find_parent_series_directories


def test_find_all_parent_series_directories(
    series_root_directory: Path,
    parent_directory_1: ParentDirectory,
    parent_directory_2: ParentDirectory,
) -> None:
    assert parent_directory_1 in find_parent_series_directories(series_root_directory)
    assert parent_directory_2 in find_parent_series_directories(series_root_directory)


def test_parent_directory_comparable_name(parent_directory_2: ParentDirectory) -> None:
    assert parent_directory_2.comparable_name == "avatar.the.last.airbender"


def test_parent_directory_assigned_files_proper_path(
    parent_directory_2: ParentDirectory,
) -> None:
    newly_assigned_files = [Path("Avatar The Last Airbender s01e02.mkv")]
    assert (
        parent_directory_2.resolve_new_file_path(newly_assigned_files[0])
        == parent_directory_2.path / "Avatar: The Last Airbender - 01x02.mkv"
    )
