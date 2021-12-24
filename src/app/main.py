"""The Main."""

import os
import json

import bobcat
import checks


def main():
    """The Main entrypoint."""
    status = bobcat.status()
    miner = bobcat.miner()
    speed = bobcat.speed()
    dig = bobcat.dig()

    print("is_healthy: " + str(checks.is_healthy(status, miner)))
    print("is_relayed: " + str(checks.is_relayed(miner)))
    print("has_errors: " + str(checks.has_errors(miner)))
    print("should_resync: " + str(checks.should_resync(status)))
    print("should_fastsync: " + str(checks.should_fastsync(status)))


if __name__ == "__main__":
    main()
