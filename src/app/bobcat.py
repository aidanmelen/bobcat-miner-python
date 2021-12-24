"""Make requests to the Bobcat miner API."""

import requests

import config


def status():
    """Get the bobcat miner status."""
    return requests.get("http://" + inputs.BOBCAT_ADDRESS + "/status.json").json()


def miner():
    """Get the bobcat miner data."""
    return requests.get("http://" + inputs.BOBCAT_ADDRESS + "/miner.json").json()


def helium_api():
    """Get the helium api data for the bobcat miner."""
    raise NotImplementedError


def onboarding():
    """Get the bobcat miner onboarding data."""
    raise NotImplementedError


def speed_test():
    """Get the bobcat miner network speed."""
    return requests.get("http://" + inputs.BOBCAT_ADDRESS + "/speed.json").json()


def resync():
    """Resync the bobcat miner."""
    raise NotImplementedError


def reset():
    """Reset the bobcat miner."""
    raise NotImplementedError


def reboot():
    """Reboot the bobcat miner."""
    raise NotImplementedError


def fastsync():
    """Fastsync the bobcat miner."""
    raise NotImplementedError


def dig():
    """Get the bobcat miner DNS data."""
    return requests.get("http://" + inputs.BOBCAT_ADDRESS + "/dig.json").json()