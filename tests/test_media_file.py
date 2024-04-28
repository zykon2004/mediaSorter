import pytest

import media_file


@pytest.mark.parametrize(
    argnames=["filename", "expected_result"],
    argvalues=[
        pytest.param(
            "The.Mandalorian.S02E02.Chapter.10.1080p.DSNP.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX.mkv",
            True,
            id="A file ending with .mkv and contains 1080p",
        ),
        pytest.param(
            "Our Wedding 2019.mkv",
            False,
            id="A file ending with .mkv but does not contain a downloaded media pattern",
        ),
    ],
)
def test_format_before_rename_raises_exceptions(
    filename: str, expected_result: bool
) -> None:
    assert media_file.is_media_file(filename) == expected_result
