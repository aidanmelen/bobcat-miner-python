"""Bobcat Miner API."""

import base64
import requests


class Bobcat:
    def __init__(self, ip_address, username="bobcat", password="miner"):
        self.ip_address = str(ip_address)
        self.username = username
        self.password = password

        self.status = None
        self.miner = None
        self.speed = None
        self.dig = None

        self.base_url = "http://" + ip_address
        base64_auth_token_bytes = base64.b64encode(
            f"{self.username}:{self.password}".encode("utf-8")
        )
        base64_auth_token = str(base64_auth_token_bytes, "utf-8")
        self.basic_auth_token_header = {"Authorization": f"Basic {base64_auth_token}"}

    def set_status(self, status):
        """Set the bobcat miner status."""
        self.status = status

    def set_miner(self, miner):
        """Set the bobcat miner data."""
        self.miner = miner

    def set_speed(self, speed):
        """Set the bobcat miner network speed."""
        self.speed = speed

    def set_dig(self, dig):
        """Set the bobcat miner DNS data."""
        self.dig = dig

    def get_status(self):
        """Get the bobcat miner status."""
        return self.status

    def get_miner(self):
        """Get the bobcat miner data."""
        return self.miner

    def get_speed(self):
        """Get the bobcat miner network speed."""
        return self.speed

    def get_dig(self):
        """Get the bobcat miner DNS data."""
        return self.dig

    def request_status(self):
        """Retreive the bobcat miner status."""
        return requests.get(self.base_url + "/status.json").json()

    def request_miner(self):
        """Retreive the bobcat miner data."""
        return requests.get(self.base_url + "/miner.json").json()

    def request_speed(self):
        """Retreive the bobcat miner network speed."""
        return requests.get(self.base_url + "/speed.json").json()

    def request_dig(self):
        """Retreive the bobcat miner DNS data."""
        return requests.get(self.base_url + "/dig.json").json()

    def request_resync(self):
        """Resync the bobcat miner."""
        return requests.post(self.base_url + "/admin/resync", header=self.basic_auth_token_header)

    def request_reset(self):
        """Reset the bobcat miner."""
        return requests.post(self.base_url + "/admin/reset", header=self.basic_auth_token_header)

    def request_reboot(self):
        """Reboot the bobcat miner."""
        return requests.post(self.base_url + "/admin/reboot", header=self.basic_auth_token_header)

    def request_fastsync(self):
        """Fastsync the bobcat miner."""
        return requests.post(self.base_url + "/admin/fastsync", header=self.basic_auth_token_header)

    def refresh(self):
        """Refresh the bobcat miner class attributes. (Warning) Frequently refreshing will degrade the bobcats performance."""
        self.set_status(self.request_status())
        self.set_miner(self.request_miner())
        self.set_speed(self.request_speed())
        self.set_dig(self.request_dig())

        return None

    def is_running(self):
        """Check if the bobcat miner is running."""
        return self.miner.get("miner", {}).get("State") == "running"

    def is_synced(self):
        """Check if the bobcat miner is synced with the Helium blockchain."""
        return self.status.get("status") == "Synced"

    def has_safe_temp(self):
        """Check if the bobcat miner is operating within a safe tempurature range."""
        temp0 = int(self.miner.get("temp0").strip(" °C"))
        temp1 = int(self.miner.get("temp1").strip(" °C"))

        return temp0 >= 0 and temp0 < 60 and temp1 >= 0 and temp1 < 60

    def has_errors(self):
        """Check for bobcat errors."""
        return self.miner["errors"] != ""

    def is_healthy(self):
        """Check if the is synced with the Helium blockchain."""
        return (
            self.is_running()
            and self.is_synced()
            and self.has_safe_temp()
            and not self.has_errors()
        )

    def is_relayed(self):
        """Check if the bobcat is being relayed."""
        for port, status in self.miner["ports"].items():
            return "44158" in port and status != "open"

    def should_fastsync(self):
        """Check if the bobcat miner needs a fastsync."""
        gap = int(self.status['gap'])
        return gap > 400 and gap < 10000

    def should_resync(self):
        """Check if the bobcat miner needs a resync."""
        gap = int(self.status['gap'])
        return gap >= 10000

    def should_reset(self):
        """Check if the bobcat miner needs to be reset."""
        gap = int(self.status['gap'])
        return self.has_errors() and gap >= 10000
