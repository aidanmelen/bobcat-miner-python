from logger import LogStreamFormatter

import logging
import requests


class BobcatBase:
    """A base class for Bobcat."""

    def __init__(self, log_level: str = "INFO") -> None:
        self.logger = logging.getLogger("bobcat")
        stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(LogStreamFormatter())
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(log_level.upper())
