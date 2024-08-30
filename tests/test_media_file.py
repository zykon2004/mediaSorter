from pathlib import Path

import pytest

from mdsort import media_file

from .consts import (
    DOWNLOADED_APP_DIRECTORY,
    DOWNLOADED_MEDIA_DIRECTORY,
    MEDIA_INDICATOR,
    MEDIA_SUFFIX,
    PERSONAL_MEDIA_DIRECTORY,
)


@pytest.mark.parametrize(
    argnames=["filename", "expected_result"],
    argvalues=[
        pytest.param(
            f"The.Mandalorian.S02E02.Chapter.10.{MEDIA_INDICATOR}.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX{MEDIA_SUFFIX}",
            True,
            id=f"A file ending with .mkv and contains {MEDIA_INDICATOR}",
        ),
        pytest.param(
            f"The.Mandalorian.S02E02.Chapter.10.{MEDIA_INDICATOR}.DSNP.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX",
            False,
            id="Contains downloaded media pattern but is not a file",
        ),
        pytest.param(
            f"Our Wedding 2019{MEDIA_SUFFIX}",
            False,
            id="A file ending with .mkv but does not contain a downloaded media pattern",
        ),
    ],
)
def test_format_before_rename_raises_exceptions(
    filename: str, expected_result: bool
) -> None:
    assert media_file.is_downloaded_media_file(Path(filename)) == expected_result


def test_find_downloaded_file_in_directory(
    downloads_directory: Path,
) -> None:
    assert media_file.is_downloaded_media_directory(
        downloads_directory / DOWNLOADED_MEDIA_DIRECTORY
    )


def test_downloaded_app_directory_is_not_recognized_as_downloaded_media_directory(
    downloads_directory: Path,
):
    assert not media_file.is_downloaded_media_directory(
        downloads_directory / DOWNLOADED_APP_DIRECTORY
    )


def test_personal_media_folder_is_not_recognized_as_downloaded_media(
    downloads_directory: Path,
):
    assert not media_file.is_downloaded_media_directory(
        downloads_directory / PERSONAL_MEDIA_DIRECTORY
    )


@pytest.mark.parametrize(
    argnames=["file", "expected_result"],
    argvalues=[
        pytest.param(
            Path(
                f"The.Mandalorian.S02E02.Chapter.10.{MEDIA_INDICATOR}.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX{MEDIA_SUFFIX}"
            ),
            True,
            id="A file downloaded file containing s02e02 pattern",
        ),
        pytest.param(
            Path(
                f"The.Ministry.of.Ungentlemanly.Warfare.2024.{MEDIA_INDICATOR}.AMZN.WEBRip.1400MB-GalaxyRG{MEDIA_SUFFIX}"
            ),
            False,
            id="Downloaded media, but not a series",
        ),
        pytest.param(
            Path("1.jpeg"),
            False,
            id="Not a media file",
        ),
        pytest.param(
            Path(f"Our Wedding 2019{MEDIA_SUFFIX}"),
            False,
            id="Not a downloaded file",
        ),
    ],
)
def test_is_series_file(file: Path, expected_result: bool) -> None:
    assert media_file.is_series_file(file) == expected_result
