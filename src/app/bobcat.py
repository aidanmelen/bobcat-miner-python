"""Make requests to the Bobcat miner API."""

import requests

import inputs


def status():
    """Get bobcat miner status."""
    return requests.get("http://" + inputs.BOBCAT_ADDRESS + "/status.json").json()


def miner():
    """Get bobcat miner data."""
    return requests.get("http://" + inputs.BOBCAT_ADDRESS + "/miner.json").json()


def speed():
    """Get bobcat miner network speed."""
    return requests.get("http://" + inputs.BOBCAT_ADDRESS + "/speed.json").json()


def dig():
    """Get bobcat miner DNS data."""
    return requests.get("http://" + inputs.BOBCAT_ADDRESS + "/dig.json").json()
