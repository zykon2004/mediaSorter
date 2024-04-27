import logging
import logging.config
import sys
from pathlib import Path


def setup_logger(filename: str = "media_sorter") -> None:
    """Setup logger that writes to console non-debug logs,
    and writes everything to a rotating file"""
    log_directory_path = Path(__file__).parents[1] / "logs"
    filename_path = log_directory_path / f"{filename}.log"
    Path.mkdir(log_directory_path, mode=0o777, exist_ok=True)

    date_format = "%Y-%m-%d %H:%M:%S"
    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "detailed": {
                "class": "logging.Formatter",
                "format": "[%(asctime)s] [%(levelname)s] %(message)s",
                "datefmt": date_format,
                "level": "DEBUG",
            },
            "less_detailed": {
                "class": "logging.Formatter",
                "format": "[%(asctime)s] %(message)s",
                "datefmt": date_format,
                "level": "INFO",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "less_detailed",
                "level": "INFO",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": filename_path,
                "mode": "a",
                "formatter": "detailed",
                "maxBytes": 1024 * 1024 * 10,  # 10MB
                "backupCount": 10,
            },
        },
        "root": {"handlers": ["console", "file"], "level": "DEBUG"},
    }

    logging.config.dictConfig(config)
    sys.excepthook = log_uncaught_exceptions


def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
