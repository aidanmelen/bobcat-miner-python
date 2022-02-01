from __future__ import annotations

import json
import os

try:
    from logger import BobcatLogger
except:
    from .logger import BobcatLogger


class BobcatBase:
    """A base class for Bobcat. This ensures the logger is available to all sub classes."""

    def __init__(self, *args, **kwargs) -> None:

        self._hostname = kwargs.pop("hostname", None)
        self._animal = kwargs.pop("animal", None)
        self._lock_file = kwargs.pop("lock_file", ".bobcat.lock")
        self._log_file = kwargs.pop("log_file", None)
        self._state_file = kwargs.pop("state_file", ".bobcat.json")
        self._dry_run = kwargs.pop("dry_run", None)
        self._verbose = kwargs.pop("verbose", False)
        self._trace = kwargs.pop("trace", False)
        self._networks = kwargs.pop("networks", ["192.168.0.0/24", "10.0.0.0/24"])

        self.__discord_webhook_url = kwargs.pop("discord_webhook_url", None)
        self.__log_level = kwargs.pop("log_level", "DEBUG")
        self.__log_level_console = kwargs.pop("log_level_console", "INFO")
        self.__log_level_file = kwargs.pop("log_level_file", "DEBUG")
        self.__log_level_discord = kwargs.pop("log_level_discord", "WARN")

        self._logger = BobcatLogger(
            log_file=self._log_file,
            discord_webhook_url=self.__discord_webhook_url,
            log_level=self.__log_level,
            log_level_console=self.__log_level_console,
            log_level_file=self.__log_level_file,
            log_level_discord=self.__log_level_discord,
        ).logger

        self._status_data = {}
        self._miner_data = {}
        self._temp_data = {}
        self._speed_data = {}
        self._dig_data = {}
