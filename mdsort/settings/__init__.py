import os

TV_SHOWS_DIRECTORY = os.getenv("TV_SHOWS_DIR") or "."
MOVIES_DIRECTORY = os.getenv("MOVIES_DIR") or "."
DOWNLOADS_DIRECTORY = os.getenv("DOWNLOADS_DIR") or "."

TORRENT_CLIENT = "qbittorrent"
FORBIDDEN_CHARACTERS = "; :".split()
UNIFIED_SEPARATOR = "."
DEFAULT_TITLE_SEPARATOR = " "
MEDIA_FILES_SUFFIXES = ".mkv .avi .mpeg .mpg".split()
DOWNLOADED_MEDIA_INDICATORS = "720p 1080p 2160p".split()
PARENT_IDENTIFIER = ".parent"
