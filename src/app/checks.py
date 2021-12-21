"""Checks for Bobcat miner."""


def is_healthy(status, miner):
    """Check if the is synced with the Helium blockchain."""
    return status["status"] == "Synced" and miner["miner"]["State"] == "running"


def is_relayed(miner):
    """Check if the bobcat is being relayed."""

    for port, status in miner["ports"].items():
        return "44158" in port and status != "open"


def has_errors(miner):
    """Check for bobcat errors."""
    return miner["errors"] != ""


def should_fastsync(status):
    """Check if the bobcat miner needs a fastsync"""
    gap = int(status["gap"])
    return gap > 400 and gap < 5000


def should_resync(status):
    """Check if the bobcat miner needs a resync."""
    gap = int(status["gap"])
    return gap > 5000


def should_reset(miner, status):
    """Check if the bobcat miner needs to be reset."""
    return not is_healthy(status, miner) and has_errors
