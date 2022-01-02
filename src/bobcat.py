"""Bobcat Miner"""

import base64
import requests

class Bobcat:
    def __init__(self, ip_address, username="bobcat", password="miner"):
        self.ip_address = str(ip_address)
        self.username = username
        self.password = password

        self.status = {}
        self.miner = {}
        self.speed = {}
        self.dig = {}

        self._set_base64_auth_token()

    def _set_base64_auth_token(self):
        """Set the base64 auth token used by post calls to the API."""
        utf8_auth_token = f"{self.username}:{self.password}".encode("utf-8")
        base64_auth_token_bytes = base64.b64encode(utf8_auth_token)
        base64_auth_token = str(base64_auth_token_bytes, "utf-8")
        self.basic_auth_token_header = {"Authorization": f"Basic {base64_auth_token}"}
        return None

    def refresh_status(self):
        """Refresh data for the bobcat miner status."""
        self.status = requests.get("http://" + self.ip_address + "/status.json").json()
        return None

    def refresh_miner(self):
        """Refresh data for the bobcat miner data."""
        self.miner = requests.get("http://" + self.ip_address + "/miner.json").json()
        return None

    def refresh_speed(self):
        """Refresh data for the bobcat miner network speed."""
        self.speed = requests.get("http://" + self.ip_address + "/speed.json").json()
        return None

    def refresh_dig(self):
        """Refresh data for the bobcat miner DNS data."""
        self.dig = requests.get("http://" + self.ip_address + "/dig.json").json()
        return None
    
    def refresh(self, status=True, miner=True, speed=True, dig=True):
        """Refresh data for the bobcat miner."""
        if status:
            self.refresh_status()
        if miner:
            self.refresh_miner()
        if speed:
            self.refresh_speed()
        if dig:
            self.refresh_dig()
        return None

    def resync(self):
        """Resync the bobcat miner."""
        return requests.post(
            "http://" + self.ip_address + "/admin/resync", header=self.basic_auth_token_header
        )

    def reset(self):
        """Reset the bobcat miner."""
        return requests.post(
            "http://" + self.ip_address + "/admin/reset", header=self.basic_auth_token_header
        )

    def reboot(self):
        """Reboot the bobcat miner."""
        return requests.post(
            "http://" + self.ip_address + "/admin/reboot", header=self.basic_auth_token_header
        )

    def fastsync(self):
        """Fastsync the bobcat miner."""
        return requests.post(
            "http://" + self.ip_address + "/admin/fastsync", header=self.basic_auth_token_header
        )

    def is_running(self):
        """Check if the bobcat miner is running."""
        return self.miner.get("miner", {}).get("State") == "running"

    def is_synced(self):
        """Check if the bobcat miner is synced with the Helium blockchain."""
        return self.status.get("status") == "Synced"

    def is_temp_safe(self):
        """Check if the bobcat miner is operating within a safe tempurature range."""
        temp0 = int(self.miner.get("temp0").strip(" °C"))
        temp1 = int(self.miner.get("temp1").strip(" °C"))

        # Operating tempuratures from bobcat user manual
        # https://fccid.io/2AZCK-MINER300/User-Manual/user-manual-5189053.pdf
        return temp0 >= 0 and temp0 < 60 and temp1 >= 0 and temp1 < 60

    def has_errors(self):
        """Check for bobcat errors."""
        return self.miner["errors"] != ""

    def is_healthy(self):
        """Check if the is synced with the Helium blockchain."""
        return (
            self.is_running() and self.is_synced() and self.is_temp_safe() and not self.has_errors()
        )

    def is_relayed(self):
        """Check if the bobcat is being relayed."""
        public_ip = self.miner.get('public_ip')
        return f"|/ip4/{public_ip}/tcp/44158|" not in self.miner.get('peerbook', [])
                
    def should_fastsync(self):
        """Check if the bobcat miner needs a fastsync."""
        gap = int(self.status["gap"])
        return gap > 400 and gap < 10000

    def should_resync(self):
        """Check if the bobcat miner needs a resync."""
        gap = int(self.status["gap"])
        return gap >= 10000
    
    def should_reboot(self):
        """Check if the bobcat miner needs to be reboot."""
        gap = int(self.status["gap"])
        return not self.has_errors() and gap <= 10000

    def should_reset(self):
        """Check if the bobcat miner needs to be reset."""
        gap = int(self.status["gap"])
        return self.has_errors() and gap > 10000
