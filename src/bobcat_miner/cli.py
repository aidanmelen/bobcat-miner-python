import logging
import os
import json
import time

try:
    from .bobcat import Bobcat
except:
    from bobcat import Bobcat

try:
    from .autopilot import Autopilot, BobcatConnectionError
except:
    from autopilot import Autopilot, BobcatConnectionError

# TODO implent click command line interface
# example: https://github.com/aidanmelen/website-checker/blob/main/src/website_checker/cli.py

def autopilot():
    """bobcat-autopilot"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    log_file = os.getenv("BOBCAT_LOG_FILE", "/var/log/bobcat-autopilot.log")
    log_level = os.getenv("BOBCAT_LOG_LEVEL", "DEBUG")
    log_discord_webhook_url = os.getenv("BOBCAT_LOG_DISCORD_WEBHOOK_URL")
    log_discord_log_level = os.getenv("BOBCAT_LOG_DISCORD_LOG_LEVEL", "DEBUG")
    dry_run = os.getenv("BOBCAT_AUTOPILOT_DRY_RUN", "False").upper() == "TRUE"

    log_levels = {
        "NOTSET": logging.NOTSET,
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    autopilot = Autopilot(
        bobcat,
        log_file=log_file,
        log_level=log_levels[log_level],
        log_discord_webhook_url=log_discord_webhook_url,
        log_discord_log_level=log_levels[log_discord_log_level],
        dry_run=dry_run,
    )
    autopilot.run()


def status():
    """bobcat-status"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    bobcat.refresh_status()
    print(json.dumps(bobcat.status_data, indent=4))


def miner():
    """bobcat-miner"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    bobcat.refresh_miner()
    print(json.dumps(bobcat.miner_data, indent=4))


def temp():
    """bobcat-temp"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    bobcat.refresh_temp()
    print(json.dumps(bobcat.temp_data, indent=4))


def speed():
    """bobcat-speed"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    bobcat.refresh_speed()
    print(json.dumps(bobcat.speed_data, indent=4))


def dig():
    """bobcat-dig"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    bobcat.refresh_dig()
    print(json.dumps(bobcat.dig_data, indent=4))


def ping():
    """bobcat-ping"""
    try:
        bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
        log_file = os.getenv("BOBCAT_LOG_FILE", "/var/log/bobcat-autopilot.log")
        log_level = os.getenv("BOBCAT_LOG_LEVEL", "DEBUG")
        log_discord_webhook_url = os.getenv("BOBCAT_LOG_DISCORD_WEBHOOK_URL")
        log_discord_log_level = os.getenv("BOBCAT_LOG_DISCORD_LOG_LEVEL", "DEBUG")
        dry_run = os.getenv("BOBCAT_AUTOPILOT_DRY_RUN", "False").upper() == "TRUE"

        log_levels = {
            "NOTSET": logging.NOTSET,
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        autopilot = Autopilot(
            bobcat,
            log_file=log_file,
            log_level=log_levels[log_level],
            log_discord_webhook_url=log_discord_webhook_url,
            log_discord_log_level=log_levels[log_discord_log_level],
            dry_run=dry_run,
        )
        autopilot.ping()
    except BobcatConnectionError:
        autopilot.logger.error(
            "The Autopilot was unable to connect to the Bobcat ({bobcat.ip_address})"
        )
    finally:
        if autopilot.log_discord_webhook_url:
            time.sleep(5)  # wait for discord logs to flush


def reboot():
    """bobcat-reboot"""
    Bobcat(os.getenv("BOBCAT_IP_ADDRESS")).reboot()


def resync():
    """bobcat-resync"""
    Bobcat(os.getenv("BOBCAT_IP_ADDRESS")).resync()


def fastsync():
    """bobcat-fastsync"""
    Bobcat(os.getenv("BOBCAT_IP_ADDRESS")).fastsync()


def reset():
    """bobcat-reset"""
    Bobcat(os.getenv("BOBCAT_IP_ADDRESS")).reset()


if __name__ == "__main__":
    autopilot()
