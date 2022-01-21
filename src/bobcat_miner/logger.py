from logging import LogRecord
from logging.handlers import TimedRotatingFileHandler
from discord_lumberjack.handlers import DiscordWebhookHandler
from discord_lumberjack.message_creators import EmbedMessageCreator

import logging


class Color:
    """A class for terminal color codes."""

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


class BobcatColorLogFormatter(logging.Formatter):
    """A class for formatting colored logs."""

    FORMAT = "%(prefix)s%(msg)s%(suffix)s"

    LOG_LEVEL_COLOR = {
        "DEBUG": {'prefix': '', 'suffix': ''},
        "INFO": {'prefix': '', 'suffix': ''},
        "WARNING": {'prefix': Color.BOLD_YELLOW, 'suffix': Color.END},
        "ERROR": {'prefix': Color.BOLD_RED, 'suffix': Color.END},
        "CRITICAL": {'prefix': Color.BOLD_RED, 'suffix': Color.END},
    }

    def format(self, record: LogRecord) -> logging.Formatter:
        """Format log records with a default prefix and suffix to terminal color codes that corresponds to the log level name."""
        if not hasattr(record, 'prefix'):
            record.prefix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get('prefix')
        
        if not hasattr(record, 'suffix'):
            record.suffix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get('suffix')

        formatter = logging.Formatter(self.FORMAT)
        return formatter.format(record)


class BobcatEmbedMessageCreator(EmbedMessageCreator):

    LOG_LEVEL_EMOJI = {
        "DEBUG": { "emoji": "🐛", "url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/320/apple/285/bug_1f41b.png"},
        "INFO": { "emoji": "🔔", "url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/320/apple/285/bell_1f514.png"},
        "WARNING": { "emoji": "⚠️", "url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/320/apple/285/warning_26a0-fe0f.png"},
        "ERROR": { "emoji": "💥", "url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/320/apple/285/police-car-light_1f6a8.png"},
        "CRITICAL": { "emoji": "🚨", "url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/320/apple/285/collision_1f4a5.png"},
    }

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
        return self.LOG_LEVEL_EMOJI.get(record.levelname.upper()).get("url")

    def get_description(self, record: LogRecord) -> None:
        """Returns the string to set the embed's description to. By default this is the path to the file and the line that the log was created at.
		You can override this method to return a custom description.
		Args:
			record (LogRecord): The `LogRecord` containing the data to use.
		Returns:
			str: The string to set the description to.
		"""
        if hasattr(record, 'description'):
            return record.description
        else:
            return ""
    