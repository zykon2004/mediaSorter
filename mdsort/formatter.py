import datetime
import re
from contextlib import suppress


FORBIDDEN_CHARACTERS = "; :".split()
UNIFIED_SEPERATOR = "."


def format_series_title_and_file_name(title: str) -> str:
    formatted_title = title.lower()
    formatted_title = create_unified_seperator(formatted_title)
    formatted_title = remove_the_prefix(formatted_title)
    formatted_title = removed_year_and_imdb_suffix(formatted_title)
    formatted_title = remove_forbidden_characters(formatted_title)
    return formatted_title


def create_unified_seperator(formatted_title):
    formatted_title = formatted_title.replace(" ", UNIFIED_SEPERATOR)
    formatted_title = formatted_title.replace("_", UNIFIED_SEPERATOR)
    return formatted_title


def remove_forbidden_characters(formatted_title: str):
    for char in FORBIDDEN_CHARACTERS:
        formatted_title = formatted_title.replace(char, "")
    return formatted_title.strip(UNIFIED_SEPERATOR)


def remove_the_prefix(formatted_title: str):
    if formatted_title.startswith(f"the{UNIFIED_SEPERATOR}"):
        formatted_title = formatted_title.removeprefix(f"the{UNIFIED_SEPERATOR}")
    return formatted_title


def removed_year_and_imdb_suffix(formatted_title: str):
    title_suffix = formatted_title.rsplit(UNIFIED_SEPERATOR, maxsplit=1)[1]
    if re.match(pattern=r"^tt\d+", string=title_suffix):
        formatted_title = formatted_title.removesuffix(title_suffix)
    with suppress(ValueError):
        if 1900 <= int(title_suffix) <= datetime.datetime.now().year:
            formatted_title = formatted_title.removesuffix(title_suffix)
    return formatted_title.strip(UNIFIED_SEPERATOR)


def format_series_filename_before_rename(filename: str): ...