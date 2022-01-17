"""Bobcat Miner Helpers"""

from logging.handlers import TimedRotatingFileHandler
from discord_lumberjack.handlers import DiscordWebhookHandler
from discord_lumberjack.message_creators import BasicMessageCreator

import logging
import os


class Color:
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


class LogLevelColor:
    TRACE = Color.WHITE
    DEBUG = Color.WHITE
    INFO = Color.BOLD_GREEN
    WARNING = Color.BOLD_YELLOW
    ERROR = Color.BOLD_RED
    CRITICAL = Color.BOLD_RED


class LogLevelEmoji:
    TRACE = ""
    DEBUG = ""
    INFO = "🔔"
    WARNING = "⚠️"
    ERROR = "💥"
    CRITICAL = "🚨"


class LogStreamFormatter(logging.Formatter):

    logging_trace = logging.DEBUG - 5

    FORMATS = {
        logging_trace: f"{LogLevelColor.TRACE}%(msg)s{Color.END}",
        logging.DEBUG: f"{LogLevelColor.DEBUG}%(msg)s{Color.END}",
        logging.INFO: f"{LogLevelColor.INFO}{LogLevelEmoji.INFO} %(msg)s{Color.END}",
        logging.WARNING: f"{LogLevelColor.WARNING}{LogLevelEmoji.WARNING} %(msg)s{Color.END}",
        logging.ERROR: f"{LogLevelColor.ERROR}{LogLevelEmoji.ERROR} %(msg)s{Color.END}",
        logging.CRITICAL: f"{LogLevelColor.CRITICAL}{LogLevelEmoji.CRITICAL} %(msg)s{Color.END}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class LogDiscordFormatter(logging.Formatter):

    logging_trace = logging.DEBUG - 5
    FORMATS = {
        logging_trace: f"{LogLevelEmoji.TRACE}%(msg)s",
        logging.DEBUG: f"{LogLevelEmoji.DEBUG}%(msg)s",
        logging.INFO: f"{LogLevelEmoji.INFO} %(msg)s",
        logging.WARNING: f"{LogLevelEmoji.WARNING} %(msg)s",
        logging.ERROR: f"{LogLevelEmoji.ERROR} %(msg)s",
        logging.CRITICAL: f"{LogLevelEmoji.CRITICAL} %(msg)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# https://stackoverflow.com/a/35804945/3894599
def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError("{} already defined in logging module".format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError("{} already defined in logging module".format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError("{} already defined in logger class".format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


def get_logger(log_level, log_file, discord_webhook_url, discord_message_monospace):
    """Get Bobcat Autopilot logger"""

    try:
        addLoggingLevel("TRACE", logging.DEBUG - 5)
    except AttributeError:
        # so unittests do not break
        pass

    LOG_LEVELS = {
        "NOTSET": logging.NOTSET,
        "TRACE": logging.TRACE,
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    logger = logging.getLogger("bobcat-autopilot")
    logger.setLevel(LOG_LEVELS[log_level])

    # for printing to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(LogStreamFormatter())
    logger.addHandler(stream_handler)

    # for writing to log file
    if log_file:
        file_handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=7)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        )
        logger.addHandler(file_handler)

    # for sending to Discord channel
    if discord_webhook_url:
        discord_webhook_handler = DiscordWebhookHandler(
            url=discord_webhook_url,
            level=log_level,
            message_creator=BasicMessageCreator(monospace=discord_message_monospace),
        )
        discord_webhook_handler.setFormatter(LogDiscordFormatter())
        logger.addHandler(discord_webhook_handler)

    return logger


# if __name__ == "__main__":
#     logger = get_logger("TRACE", None, os.getenv("BOBCAT_DISCORD_WEBHOOK_URL"))
#     logger.debug("🚀 The Bobcat Autopilot is starting")
#     logger.debug("Ping the Bobcat (192.168.0.10)")
#     logger.info("Successfully pinged the Bobcat")
#     logger.debug("Refreshing Bobcat endpoints")
#     logger.info("Successfully refreshed Bobcat endpoints")
#     logger.debug("👀 Checking Bobcat relay")
#     logger.info("The Bobcat's activity is not relayed")
#     logger.debug("👀 Checking Bobcat CPU tempurature")
#     logger.info("The Bobcat's CPU tempurature is good")
#     logger.debug("👀 Checking Bobcat network speed")
#     logger.info("The Bobcat's network speed is good")
#     logger.debug("👀 Checking Bobcat miner API data for errors")
#     logger.info("The Bobcat is healthy")
#     logger.debug("🏁 The Bobcat Autopilot is finished")
