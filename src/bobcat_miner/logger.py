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
        


if __name__ == "__main__":
    import os
    import json

    discord_webhook_url = os.getenv("BOBCAT_DISCORD_WEBHOOK_URL")

    logger = logging.getLogger('bobcat')
    logger.setLevel('DEBUG')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(BobcatColorLogFormatter())
    logger.addHandler(stream_handler)

    discord_webhook_handler = DiscordWebhookHandler(
        url=discord_webhook_url,
        level="DEBUG",
        message_creator=BobcatEmbedMessageCreator(),
    )
    logger.addHandler(discord_webhook_handler)


    # logger.debug("This is debug")
    # logger.info("This is info")
    # logger.info("This is a green info", extra={'prefix': Color.GREEN, 'suffix': Color.END})
    # logger.warning("This is warning")
    dump = json.dumps({
        "ota_version": "1.0.2.75",
        "region": "region_us915",
        "frequency_plan": "us915",
        "animal": "merry-peanut-swan",
        "pubkey": "112YUS4TUQy4boXRvGjrj6z7XyiSx8FDumTn6vtRYPgoGPnjBGWW",
        "miner": {
            "State": "running",
            "Status": "Up 9 hours",
            "Names": [
            "/miner"
            ],
            "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
            "Created": 1642707773
        },
        "p2p_status": [
            "+---------+-------+",
            "|  name   |result |",
            "+---------+-------+",
            "|connected|  yes  |",
            "|dialable |  yes  |",
            "|nat_type | none  |",
            "| height  |1191075|",
            "+---------+-------+",
            "",
            ""
        ],
        "miner_height": "1191075",
        "epoch": "31417",
        "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
        "ports": {
            "192.168.0.8:22": "open",
            "192.168.0.8:44158": "open",
            "97.117.96.28:22": "closed/timeout",
            "97.117.96.28:44158": "closed/timeout"
        },
        "private_ip": "192.168.0.8",
        "public_ip": "97.117.96.28",
        "peerbook": [
            "+-----------------------------------------------+--------------+----------+---------+---+----------+",
            "|                    address                    |     name     |listen_add|connectio|nat|last_updat|",
            "+-----------------------------------------------+--------------+----------+---------+---+----------+",
            "|/p2p/112YUS4TUQy4boXRvGjrj6z7XyiSx8FDumTn6vtRYP|merry-peanut-s|    1     |   11    |non| 232.266s |",
            "+-----------------------------------------------+--------------+----------+---------+---+----------+",
            "",
            "+---------------------------+",
            "|listen_addrs (prioritized) |",
            "+---------------------------+",
            "|/ip4/97.117.96.28/tcp/44158|",
            "+---------------------------+",
            "",
            "+------------------+--------------------+----------------------------------------+-----------------+",
            "|      local       |       remote       |                  p2p                   |      name       |",
            "+------------------+--------------------+----------------------------------------+-----------------+",
            "|/ip4/172.17.0.2/tc|/ip4/35.161.222.43/t|/p2p/1127gHz2sKqNJXQN8an6mNu1U3RusHyXkqp|broad-iris-sheep |",
            "|/ip4/172.17.0.2/tc|/ip4/88.247.226.194/|/p2p/112KNNxS6u6k1QBmin7226f3YQbscLx5mr4|damp-chili-buffal|",
            "|/ip4/172.17.0.2/tc|/ip4/24.136.15.5/tcp|/p2p/112QSKdtAGBq56X2rpoxEkTjKUVLDsBu13u|oblong-mint-seagu|",
            "|/ip4/172.17.0.2/tc|/ip4/68.98.24.140/tc|/p2p/112Wt5P3kRRr7HZynDozBG2Tvc1YvRJySYo|quick-olive-falco|",
            "|/ip4/172.17.0.2/tc|/ip4/3.141.114.10/tc|/p2p/112dADs1gLzPckMkkjDdk9ihp1EdEQmVw5i|recumbent-fuzzy-s|",
            "|/ip4/172.17.0.2/tc|/ip4/223.223.217.171|/p2p/112vS2Nj7C8Bttbw3qF3JdWmH424vTKyRpP|massive-crimson-d|",
            "|/ip4/172.17.0.2/tc|/ip4/2.140.28.128/tc|/p2p/114yXBC5sqYjhMAYW3MZesosR7Bwi1dt9hB|dapper-burgundy-d|",
            "|/ip4/172.17.0.2/tc|/ip4/31.20.237.17/tc|/p2p/11sBMdU1SDEbcgLTDGKsb5jYWPE6FdKUy4K|sneaky-felt-parro|",
            "|/ip4/172.17.0.2/tc|/ip4/34.150.15.153/t|/p2p/13GL7mzrn1uszHMfCenVW3vwcgVRwTyibMx|micro-carrot-octo|",
            "+------------------+--------------------+----------------------------------------+-----------------+",
            "",
            ""
        ],
        "height": [
            "31417    1191075",
            ""
        ],
        "temp0": "29 °C",
        "temp1": "28 °C",
        "timestamp": "2022-01-21 04:22:38 +0000 UTC",
        "errors": ""
        },
        indent=4
    )
    logger.error("This is error", extra={"description": f"```{dump}```"})
    # logger.critical("This is critical")

    