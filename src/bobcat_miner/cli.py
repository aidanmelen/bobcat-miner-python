import logging
import os
import json

try:
    from .bobcat import Bobcat
except:
    from bobcat import Bobcat

try:
    from .autopilot import Autopilot, BobcatConnectionError
except:
    from autopilot import Autopilot, BobcatConnectionError


def autopilot():
    """bobcat-autopilot"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    log_file = os.getenv("BOBCAT_AUTOPILOT_LOG_FILE", "/var/log/bobcat-autopilot.log")
    log_level = os.getenv("BOBCAT_AUTOPILOT_LOG_LEVEL", logging.DEBUG)
    discord_webhook_url = os.getenv("BOBCAT_DISCORD_WEBHOOK", None)
    dry_run = os.getenv("BOBCAT_AUTOPILOT_DRY_RUN", "False").upper() == "TRUE"

    autopilot = Autopilot(bobcat, log_file=log_file, log_level=log_level, discord_webhook_url=discord_webhook_url, dry_run=dry_run)
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
        log_file = os.getenv("BOBCAT_AUTOPILOT_LOG_FILE", "/var/log/bobcat-autopilot.log")
        log_level = os.getenv("BOBCAT_AUTOPILOT_LOG_LEVEL", logging.DEBUG)
        dry_run = os.getenv("BOBCAT_AUTOPILOT_DRY_RUN", "False").upper() == "TRUE"

        autopilot = Autopilot(bobcat, log_file=log_file, log_level=log_level, dry_run=dry_run)
        autopilot.ping()
    except BobcatConnectionError:
        autopilot.logger.error(
            "The Autopilot was unable to connect to the Bobcat ({bobcat.ip_address})"
        )


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
