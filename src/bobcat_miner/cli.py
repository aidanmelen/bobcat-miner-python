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


def status():
    """bobcat-status"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    bobcat.refresh_status()
    print(json.dumps(bobcat.status, indent=4))


def miner():
    """bobcat-miner"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    bobcat.refresh_miner()
    print(json.dumps(bobcat.miner, indent=4))


def speed():
    """bobcat-speed"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    bobcat.refresh_speed()
    print(json.dumps(bobcat.speed, indent=4))


def dig():
    """bobcat-dig"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    bobcat.refresh_dig()
    print(json.dumps(bobcat.dig, indent=4))


def reboot():
    """bobcat-reboot"""
    print(Bobcat(os.getenv("BOBCAT_IP_ADDRESS")).reboot())


def resync():
    """bobcat-resync"""
    print(Bobcat(os.getenv("BOBCAT_IP_ADDRESS")).resync())


def fastsync():
    """bobcat-fastsync"""
    print(Bobcat(os.getenv("BOBCAT_IP_ADDRESS")).fastsync())


def reset():
    """bobcat-reset"""
    print(Bobcat(os.getenv("BOBCAT_IP_ADDRESS")).reset())


def autopilot():
    """bobcat-autopilot"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))

    autopilot = Autopilot(bobcat)
    autopilot.run()


if __name__ == "__main__":
    autopilot()
