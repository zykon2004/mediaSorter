import pytest

import converter


@pytest.mark.parametrize(
    argnames=["title", "converted_title"],
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
            "Catch 22 tt5056196",
            "catch.22",
            id="removed imdb identifier",
        ),
        pytest.param(
            "Avatar: The Last Airbender tt9018736",
            "avatar.the.last.airbender",
            id="removed imdb identifier and :",
        ),
    ],
)
def test_rename_series_title(title: str, converted_title: str):
    assert converter.convert_series_title(title) == converted_title
