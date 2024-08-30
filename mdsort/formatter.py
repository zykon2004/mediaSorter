import datetime
import re
from contextlib import suppress

import settings

FIRST_TV_SHOW_RELEASE_YEAR = 1934


def format_series_title_and_file_name(title: str) -> str:
    formatted_title = title.lower()
    formatted_title = create_unified_separator(formatted_title)
    formatted_title = remove_the_prefix(formatted_title)
    formatted_title = removed_year_and_imdb_suffix(formatted_title)
    return remove_forbidden_characters(formatted_title)


def create_unified_separator(formatted_title: str) -> str:
    formatted_title = formatted_title.replace(" ", settings.UNIFIED_SEPARATOR)
    return formatted_title.replace("_", settings.UNIFIED_SEPARATOR)


def remove_forbidden_characters(formatted_title: str) -> str:
    for char in settings.FORBIDDEN_CHARACTERS:
        formatted_title = formatted_title.replace(char, "")
    return formatted_title.strip(settings.UNIFIED_SEPARATOR)


def remove_the_prefix(
    formatted_title: str, separator: str = settings.UNIFIED_SEPARATOR
) -> str:
    if formatted_title.startswith(f"The{separator}"):
        prefix_to_remove = f"The{separator}"
    elif formatted_title.startswith(f"the{separator}"):
        prefix_to_remove = f"the{separator}"
    else:
        prefix_to_remove = ""

    return formatted_title.removeprefix(prefix_to_remove)


def removed_year_and_imdb_suffix(
    formatted_title: str, separator: str = settings.UNIFIED_SEPARATOR
) -> str:
    title_suffix = formatted_title.rsplit(separator, maxsplit=1)[1]
    if re.match(pattern=r"^tt\d+", string=title_suffix):
        formatted_title = formatted_title.removesuffix(title_suffix)
    with suppress(ValueError):
        if (
            FIRST_TV_SHOW_RELEASE_YEAR
            <= int(title_suffix)
            <= datetime.datetime.now(tz=datetime.UTC).year
        ):
            formatted_title = formatted_title.removesuffix(title_suffix)
    return formatted_title.strip(separator)


def extract_season_and_episode_from_series_filename(filename: str) -> tuple[str, str]:
    series_season_and_episode_match = re.search(r"s\d\de\d\d", filename, re.IGNORECASE)
    if series_season_and_episode_match:
        series_season_and_episode = series_season_and_episode_match[0]
        return series_season_and_episode[1:3], series_season_and_episode[4:]

    raise SeasonEpisodePatternNotFound(f"Didn't find S01E01 pattern in {filename}")


def format_series_filename_before_rename(filename: str, title: str) -> str:
    season, episode = extract_season_and_episode_from_series_filename(filename)
    formatted_title = removed_year_and_imdb_suffix(
        title, separator=settings.DEFAULT_TITLE_SEPARATOR
    )
    formatted_title = remove_the_prefix(
        formatted_title, separator=settings.DEFAULT_TITLE_SEPARATOR
    )
    return (
        f"{formatted_title} - {season}x{episode}.{filename.rsplit('.', maxsplit=1)[1]}"
    )


class SeasonEpisodePatternNotFound(Exception):
    pass
