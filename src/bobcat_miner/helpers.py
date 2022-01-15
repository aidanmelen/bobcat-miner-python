from logging.handlers import TimedRotatingFileHandler

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


def get_logger(log_file, log_level):
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

    return logger
