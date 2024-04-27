import datetime
import re
from contextlib import suppress


FORBIDDEN_CHARACTERS = "; :".split()


def convert_series_title(title: str):
    converted_title = title.lower()
    converted_title = remove_the_prefix(converted_title)
    converted_title = removed_year_and_imdb_suffix(converted_title)
    converted_title = remove_forbidden_characters(converted_title)
    return converted_title.strip()


def remove_forbidden_characters(converted_title: str):
    for char in FORBIDDEN_CHARACTERS:
        converted_title = converted_title.replace(char, "")
    return converted_title


def remove_the_prefix(converted_title: str):
    if converted_title.startswith("the "):
        converted_title = converted_title.removeprefix("the ")
    return converted_title


def removed_year_and_imdb_suffix(converted_title: str):
    title_suffix = converted_title.rsplit(" ", maxsplit=1)[1]
    if re.match(pattern=r"^tt\d+", string=title_suffix):
        converted_title = converted_title.removesuffix(title_suffix)
    with suppress(ValueError):
        if 1900 <= int(title_suffix) <= datetime.datetime.now().year:
            converted_title = converted_title.removesuffix(title_suffix)
    return converted_title
