import os

TV_SHOWS_DIRECTORY = os.getenv("TV_SHOWS_DIR")
if not TV_SHOWS_DIRECTORY:
    raise ValueError("TV_SHOW_DIR not supplied")
MOVIES_DIRECTORY = os.getenv("MOVIES_DIR")
if not MOVIES_DIRECTORY:
    raise ValueError("MOVIES_DIR not supplied")
DOWNLOADS_DIRECTORY = os.getenv("DOWNLOADS_DIR")
if not DOWNLOADS_DIRECTORY:
    raise ValueError("DOWNLOADS_DIR not supplied")

TORRENT_CLIENT = "qbittorrent"
FORBIDDEN_CHARACTERS = "; :".split()
UNIFIED_SEPARATOR = "."
DEFAULT_TITLE_SEPARATOR = " "
MEDIA_FILES_SUFFIXES = ".mkv .avi .mpeg .mpg".split()
DOWNLOADED_MEDIA_INDICATORS = "720p 1080p 2160p".split()
PARENT_IDENTIFIER = ".parent"
