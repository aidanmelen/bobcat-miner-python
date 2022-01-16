from logging.handlers import TimedRotatingFileHandler
from discord_lumberjack.handlers import DiscordWebhookHandler

import logging


class Color:
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


class StdoutColorFormatter(logging.Formatter):

    format = "%(message)s"
    FORMATS = {
        logging.DEBUG: Color.WHITE + format + Color.END,
        logging.INFO: Color.BOLD + Color.GREEN + format + Color.END,
        logging.WARNING: Color.BOLD + Color.YELLOW + format + Color.END,
        logging.ERROR: Color.BOLD + Color.RED + format + Color.END,
        logging.CRITICAL: Color.BOLD + Color.RED + format + Color.END,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(log_file, log_level, log_discord_webhook_url, log_discord_log_level):
    """Get Bobcat Autopilot logger"""
    logger = logging.getLogger("bobcat-autopilot")
    logger.setLevel(log_level)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(StdoutColorFormatter())
    logger.addHandler(stdout_handler)

    if log_file:
        file_handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=7)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        )
        logger.addHandler(file_handler)

    if log_discord_webhook_url:
        discord_webhook_handler = DiscordWebhookHandler(
            url=log_discord_webhook_url, level=log_discord_log_level
        )
        logger.addHandler(discord_webhook_handler)

    return logger


if __name__ == "__main__":
    import os
    import requests
    import time

    log_file = os.getenv("BOBCAT_LOG_FILE", "/var/log/bobcat-autopilot.log")
    log_level = os.getenv("BOBCAT_LOG_LEVEL", logging.DEBUG)
    log_discord_webhook_url = os.getenv("BOBCAT_LOG_DISCORD_WEBHOOK_URL")

    logger = get_logger(
        log_file=log_file, log_level=log_level, log_discord_webhook_url=log_discord_webhook_url
    )

    logger.info("i am a bobcat info")
    logger.warning("i am a bobcat warning")
    logger.error("i am a sad bobcat error")

    # requests.post(log_discord_webhook_url, { "content": "post command" })
    time.sleep(1)
