import logging

import psutil

import settings


class TorrentClientIsRunningException(Exception): ...


def is_running(process_name: str = settings.TORRENT_CLIENT) -> bool:
    _is_process_running = process_name in (p.name() for p in psutil.process_iter())
    if _is_process_running:
        logging.info("%s is running, Exiting...")
        raise TorrentClientIsRunningException
    return _is_process_running
