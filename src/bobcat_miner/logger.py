from __future__ import annotations
from dataclasses import dataclass
from logging import LogRecord
from logging.handlers import TimedRotatingFileHandler
from discord_lumberjack.handlers import DiscordWebhookHandler
from discord_lumberjack.message_creators import EmbedMessageCreator

import logging


class BobcatLogger:
    """A class for the Bobcat Logger."""

    def __init__(
        self,
        log_file: str = None,
        discord_webhook_url: str = None,
        log_level: str = "DEBUG",
        log_level_console: str = "INFO",
        log_level_file: str = "DEBUG",
        log_level_discord: str = "INFO",
    ) -> None:

        self._logger = logging.getLogger("bobcat")
        self._logger.setLevel(log_level)

        self.add_log_console_handler(log_level_console)

        if log_file:
            self.add_log_file_handler(log_file, log_level_file)

        if discord_webhook_url:
            self.add_log_discord_handler(discord_webhook_url, log_level_discord)

    @property
    def logger(self) -> BobcatLogger:
        """Return logger.
        Returns:
            (BobcatLogger): The instance of the BobcatLogger.
        """
        return self._logger

    def add_log_console_handler(self, log_level: str) -> None:
        """Add the console log handler to the logger.
        Args:
            log_level (str): The log level for the console log handler.
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level.upper())
        console_handler.setFormatter(BobcatLogConsoleFormatter())
        self._logger.addHandler(console_handler)

    def add_log_file_handler(self, log_file: str, log_level: str) -> None:
        """Add the file log handler to the logger.
        Args:
            log_file (str): The log level for the file log handler.
            log_level (str): The log level for the file log handler.
        """
        file_handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=7)
        file_handler.setLevel(log_level.upper())
        file_handler.setFormatter(BobcatLogFileFormatter())
        self._logger.addHandler(file_handler)

    def add_log_discord_handler(self, discord_webhook_url: str, log_level: str) -> None:
        """Add the Discord log handler to the logger.
        Args:
            discord_webhook_url (str): The Discord webhook url where log events will be sent.
            log_level (str): The log level for the discord channel log handler.
        """

        discord_webhook_handler = DiscordWebhookHandler(
            url=discord_webhook_url,
            level=log_level.upper(),
            message_creator=BobcatEmbedMessageCreator(),
        )
        self._logger.addHandler(discord_webhook_handler)

        logging.getLogger("discord_lumberjack").setLevel(logging.ERROR)


@dataclass
class Color:
    """A class for console color codes."""

    BOLD = "\033[1m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD_WHITE = BOLD + WHITE
    BOLD_BLUE = BOLD + BLUE
    BOLD_GREEN = BOLD + GREEN
    BOLD_YELLOW = BOLD + YELLOW
    BOLD_RED = BOLD + RED
    END = "\033[0m"


LOG_LEVEL_EMOJI = {
    "DEBUG": {
        "emoji": "🐛",
        "url": "https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/bug.png",
    },
    "INFO": {
        "emoji": "✅",
        "url": "https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/check-mark-button.png",
    },
    "WARNING": {
        "emoji": "⚠️",
        "url": "https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/warning.png",
    },
    "ERROR": {
        "emoji": "❌",
        "url": "https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/cross-mark.png",
    },
    "CRITICAL": {
        "emoji": "💥",
        "url": "https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/collision.png",
    },
}


class BobcatLogFileFormatter(logging.Formatter):
    """A class for formatting logs in the file."""

    FORMAT = "%(asctime)s %(name)s %(levelname)s %(msg)s%(description)s"

    def format(self, record: LogRecord) -> LogRecord:
        """Format log records with description attribute
        Args:
            record (LogRecord): The log record to format.
        Returns:
            (LogRecord): The formatted log record.
        """

        if not hasattr(record, "description"):
            record.description = ""

        formatter = logging.Formatter(self.FORMAT)
        return formatter.format(record)


# https://stackoverflow.com/a/70796089/3894599
class BobcatLogConsoleFormatter(logging.Formatter):
    """A class for formatting colored logs in the console."""

    FORMAT = "%(prefix)s%(emoji)s%(emoji_separator)s%(msg)s%(suffix)s%(description)s"

    LOG_LEVEL_COLOR = {
        "DEBUG": {"prefix": "", "suffix": ""},
        "INFO": {"prefix": Color.GREEN, "suffix": Color.END},
        "WARNING": {"prefix": Color.YELLOW, "suffix": Color.END},
        "ERROR": {"prefix": Color.RED, "suffix": Color.END},
        "CRITICAL": {"prefix": Color.BOLD_RED, "suffix": Color.END},
    }

    EMOJI_SEPARATOR = " "
    DESCRIPTION_SEPARATOR = " "

    def format(self, record: LogRecord) -> LogRecord:
        """Format log records with a default prefix and suffix to terminal color codes that corresponds to the log level name.
        Args:
            record (LogRecord): The log record to format.
        Returns:
            (LogRecord): The formatted log record.
        """
        if not hasattr(record, "prefix"):
            record.prefix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get("prefix")

        if not hasattr(record, "emoji"):
            record.emoji = LOG_LEVEL_EMOJI.get(record.levelname.upper()).get("emoji")

        if not hasattr(record, "emoji_separator"):
            record.emoji_separator = self.EMOJI_SEPARATOR

        if not hasattr(record, "suffix"):
            record.suffix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get("suffix")

        if not hasattr(record, "description"):
            record.description = ""

        formatter = logging.Formatter(self.FORMAT)
        return formatter.format(record)


class BobcatEmbedMessageCreator(EmbedMessageCreator):
    def __init__(self):
        super().__init__()

    def get_author_icon_url(self, record: LogRecord) -> str:
        """Returns the string to set the embed's author's icon URL to. By default this is an appropriate image corresponding to the log level.
        You can override this method to return a custom icon URL.
        Args:
                record (LogRecord): The `LogRecord` containing the data to use.
        Returns:
                str: The URL to set the author's icon to.
        """
        return LOG_LEVEL_EMOJI.get(record.levelname.upper()).get("url")

    def get_author_name(self, record: LogRecord) -> str:
        """Returns the string to set the embed's author's name to. By default this is the name of the log level. FOr example "ERROR", "INFO", etc.
        You can override this method to return a custom name.
        Args:
            record (LogRecord): The `LogRecord` containing the data to use.
        Returns:
            str: The string to set the author's name to.
        """
        return f"Bobcat {record.levelname.capitalize()}"

    def get_description(self, record: LogRecord) -> None:
        """Returns the string to set the embed's description to. By default this is the path to the file and the line that the log was created at.
        You can override this method to return a custom description.
        Args:
                record (LogRecord): The `LogRecord` containing the data to use.
        Returns:
                str: The string to set the description to.
        """
        if hasattr(record, "description"):
            if record.description:
                return f"{record.description}"
        return ""
