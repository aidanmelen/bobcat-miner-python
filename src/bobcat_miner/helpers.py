from logging.handlers import TimedRotatingFileHandler
from discord_lumberjack.handlers import DiscordWebhookHandler

import logging
import os


LOG_LEVELS = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


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
    DEBUG = Color.WHITE
    INFO = Color.BOLD_GREEN
    WARNING = Color.BOLD_YELLOW
    ERROR = Color.BOLD_RED
    CRITICAL = Color.BOLD_RED


class LogLevelEmoji:
    DEBUG = ""
    INFO = "🔔"
    WARNING = "⚠️"
    ERROR = "💥"
    CRITICAL = "🚨"


class LogStreamFormatter(logging.Formatter):

    FORMATS = {
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

    # TODO multiline log message not rendering properly
    # FORMATS = {
    #     logging.DEBUG: f"{LogLevelEmoji.DEBUG}%(msg)s",
    #     logging.INFO: f"```diff\n+ {LogLevelEmoji.INFO} %(msg)s\n```",
    #     logging.WARNING: f"```fix\n{LogLevelEmoji.WARNING} %(msg)s\n```",
    #     logging.ERROR: f"```diff\n- {LogLevelEmoji.ERROR} %(msg)s\n```",
    #     logging.CRITICAL: f"```diff\n- {LogLevelEmoji.CRITICAL} %(msg)s\n```",
    # }
    FORMATS = {
        logging.DEBUG: f"%(msg)s",
        logging.INFO: f"{LogLevelEmoji.INFO} %(msg)s",
        logging.WARNING: f"{LogLevelEmoji.WARNING} %(msg)s",
        logging.ERROR: f"{LogLevelEmoji.ERROR} %(msg)s",
        logging.CRITICAL: f"{LogLevelEmoji.CRITICAL} %(msg)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(log_level, log_file, discord_webhook_url):
    """Get Bobcat Autopilot logger"""
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
        discord_webhook_handler = DiscordWebhookHandler(url=discord_webhook_url, level=log_level)
        discord_webhook_handler.setFormatter(LogDiscordFormatter())
        logger.addHandler(discord_webhook_handler)

    return logger


# if __name__ == "__main__":
#     logger = get_logger("DEBUG", None, os.getenv("BOBCAT_DISCORD_WEBHOOK_URL"))
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
