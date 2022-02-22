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
        self._dry_run = kwargs.pop("dry_run", None)
        self._no_wait = kwargs.pop("no_wait", None)
        self._trace = kwargs.pop("trace", False)
        self._networks = kwargs.pop(
            "networks",
            [
                "192.168.0.0/24",
                "10.0.0.0/24",
                "172.16.0.0/24",
                "192.168.0.1/16",
                "10.0.0.1/16",
                "172.16.0.1/16",
            ],
        )

        self.logger = BobcatLogger(
            log_file=kwargs.pop("log_file", None),
            discord_webhook_url=kwargs.pop("discord_webhook_url", None),
            log_level=kwargs.pop("log_level", "DEBUG"),
            log_level_console=kwargs.pop("log_level_console", "INFO"),
            log_level_file=kwargs.pop("log_level_file", "DEBUG"),
            log_level_discord=kwargs.pop("log_level_discord", "WARN"),
        ).logger

        self._status_data = {}
        self._miner_data = {}
        self._temp_data = {}
        self._speed_data = {}
        self._dig_data = {}
