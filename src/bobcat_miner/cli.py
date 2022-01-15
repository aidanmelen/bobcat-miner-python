import os
import json

try:
    from .bobcat import Bobcat
except:
    from bobcat import Bobcat

try:
    from .autopilot import Autopilot
except:
    from autopilot import Autopilot


def autopilot():
    """bobcat-autopilot"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    autopilot = Autopilot(bobcat)
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
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    autopilot = Autopilot(bobcat)
    autopilot.ping()


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
