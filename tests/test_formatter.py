from contextlib import nullcontext
from typing import ContextManager

import pytest

import formatter


@pytest.mark.parametrize(
    argnames=["title", "formatted_title"],
    argvalues=[
        pytest.param(
            "Catch 22",
            "catch.22",
            id="number is not removed since it is not a year",
        ),
        pytest.param(
            "The Mandalorian 2018",
            "mandalorian",
            id="Removed `The`, lower, removed Year",
        ),
        pytest.param(
            "Catch 22_tt5056196",
            "catch.22",
            id="removed imdb identifier and unified seperator",
        ),
        pytest.param(
            "Avatar: The Last Airbender tt9018736",
            "avatar.the.last.airbender",
            id="removed imdb identifier and :",
        ),
        pytest.param(
            "The.Mandalorian.S02E02.Chapter.10.1080p.DSNP.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX.mkv",
            "mandalorian.s02e02.chapter.10.1080p.dsnp.web-dl.ddp.5.1.atmos.h.264-phoenix.mkv",
            id="series file name - lower, without `the`",
        ),
        pytest.param(
            "S.W.A.T.2017.S07E10.1080p_HDTV_;;x265-MiNX[TGx]",
            "s.w.a.t.2017.s07e10.1080p.hdtv.x265-minx[tgx]",
            id="series file name - lower, forbidden, unified",
        ),
    ],
)
def test_format_series_title_and_filename(title: str, formatted_title: str) -> None:
    assert formatter.format_series_title_and_file_name(title) == formatted_title


@pytest.mark.parametrize(
    argnames=["title", "filename", "expected_result"],
    argvalues=[
        pytest.param(
            "The Office tt0386676",
            "The.Mandalorian.S02E02.Chapter.10.1080p.DSNP.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX.mkv",
            False,
            id="mismatched title and filename",
        ),
        pytest.param(
            "Mandalorian 2018",
            "The.Mandalorian.S02E02.Chapter.10.1080p.DSNP.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX.mkv",
            True,
            id="matching title and filename, removing `the`, removing suffix",
        ),
    ],
)
def test_e2e_format_series_title_and_filename(
    title: str, filename: str, expected_result: bool
) -> None:
    formatted_title = formatter.format_series_title_and_file_name(title)
    formatted_filename = formatter.format_series_title_and_file_name(filename)
    assert formatted_filename.startswith(formatted_title) == expected_result


@pytest.mark.parametrize(
    argnames=["filename", "title", "expected_filename"],
    argvalues=[
        pytest.param(
            "The.Mandalorian.S02E02.Chapter.10.1080p.DSNP.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX.mkv",
            "The Mandalorian 2018",
            "Mandalorian - 02x02.mkv",
            id="Normal case. prefix deleted, capitalized, episode and season extracted",
        ),
        pytest.param(
            "S.W.A.T.2017.S07E10.1080p_HDTV_;;x265-MiNX[TGx].avi",
            "S.W.A.T 2017",
            "S.W.A.T - 07x10.avi",
            id="avi file, dots in name",
        ),
    ],
)
def test_format_series_filename_before_rename(
    filename: str, title: str, expected_filename: str
) -> None:
    assert (
        formatter.format_series_filename_before_rename(filename, title)
        == expected_filename
    )


@pytest.mark.parametrize(
    argnames=["filename", "title", "context"],
    argvalues=[
        pytest.param(
            "The.Mandalorian.S02E02.Chapter.10.1080p.DSNP.WEB-DL.DDP.5.1.Atmos.H.264-PHOENiX.mkv",
            "The Mandalorian 2018",
            nullcontext(),
            id="No exception is raised. season, episode format found",
        ),
        pytest.param(
            "S.W.A.T 2017",
            "S.W.A.T 2017",
            pytest.raises(formatter.SeasonEpisodePatternNotFound),
            id="Did not found S01E01 pattern",
        ),
    ],
)
def test_format_before_rename_raises_exceptions(
    filename: str, title: str, context: ContextManager
) -> None:
    with context:
        formatter.format_series_filename_before_rename(filename, title)
