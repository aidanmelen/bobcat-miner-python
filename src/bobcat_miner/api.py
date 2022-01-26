from typing import List

import time

try:
    from connection import BobcatConnection
except:
    from .connection import BobcatConnection
try:
    from constants import *
except:
    from .constants import *


class BobcatAPI(BobcatConnection):
    """A class for interacting with the Bobcat API endpoints."""

    def __init__(
        self,
        hostname: str = None,
        animal: str = None,
        networks: List[str] = ["192.168.0.0/24", "10.0.0.0/24"],
        dry_run: bool = False,
        logger: str = None,
    ) -> None:
        super().__init__(hostname, animal, networks, logger)

        self.dry_run = dry_run

        self.status_data = {}
        self.miner_data = {}
        self.temp_data = {}
        self.speed_data = {}
        self.dig_data = {}

    def refresh_status(self) -> None:
        """Refresh Bobcat status data."""
        self.logger.debug("Refresh Bobcat status data")
        self.status_data = self._BobcatConnection__get(
            "http://" + self.hostname + "/status.json"
        ).json()

        if self.status_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_status()

    def refresh_miner(self) -> None:
        """Refresh Bobcat miner data."""
        self.logger.debug("Refresh Bobcat miner data")
        self.miner_data = self._BobcatConnection__get(
            "http://" + self.hostname + "/miner.json"
        ).json()

        if self.miner_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_miner()

    def refresh_speed(self) -> None:
        """Refresh Bobcat network speed data."""
        self.logger.debug("Refresh Bobcat network speed data")
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4407606223899-Netspeed-Blockchain-Reboot
        self.speed_data = self._BobcatConnection__get(
            "http://" + self.hostname + "/speed.json"
        ).json()

        if (self.speed_data == {"message": "rate limit exceeded"}) or (
            self.speed_data
            == {
                "DownloadSpeed": "",
                "UploadSpeed": "",
                "Latency": "",
            }  # https://github.com/aidanmelen/bobcat-miner-python/issues/6
        ):
            time.sleep(30)
            self.refresh_speed()

    def refresh_temp(self) -> None:
        """Refresh Bobcat temperature data."""
        self.logger.debug("Refresh Bobcat temperature data")
        self.temp_data = self._BobcatConnection__get(
            "http://" + self.hostname + "/temp.json"
        ).json()

        if self.temp_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_temp()

    def refresh_dig(self) -> None:
        """Refresh Bobcat DNS data."""
        self.logger.debug("Refresh Bobcat DNS data")
        self.dig_data = self._BobcatConnection__get("http://" + self.hostname + "/dig.json").json()

        if self.dig_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_dig()

    def refresh(
        self,
        status: bool = True,
        miner: bool = True,
        temp: bool = True,
        speed: bool = True,
        dig: bool = True,
    ) -> None:
        """Refresh data for the Bobcat."""
        if status:
            self.refresh_status()
        if miner:
            self.refresh_miner()
        if speed:
            self.refresh_speed()
        if temp:
            self.refresh_temp()
        if dig:
            self.refresh_dig()

    def reboot(self) -> str:
        """Reboot the Bobcat."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4407606223899-Netspeed-Blockchain-Reboot
        if self.dry_run:
            self.logger.warning("Dry run is enabled: Reboot Skipped")
            return "Dry run is enabled: Normally this would show the Reboot response"

        self.logger.info("Reboot Bobcat")
        return self._BobcatConnection__post("http://" + self.hostname + "/admin/reboot")

    def reset(self) -> str:
        """Reset the Bobcat."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4412997563931-Reset-Miner-Feature
        if self.dry_run:
            self.logger.warning("Dry run is enabled: Reset Skipped")
            return "Dry run is enabled: Normally this would show the Reset response"

        self.logger.info("Reset Bobcat")
        return self._BobcatConnection__post("http://" + self.hostname + "/admin/reset")

    def resync(self) -> str:
        """Resync the Bobcat."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4413004114075-Resync-Feature-
        if self.dry_run:
            self.logger.warning("Dry run is enabled: Resync Skipped")
            return "Dry run is enabled: Normally this would show the Resync response"

        self.logger.info("Resync Bobcat")
        return self._BobcatConnection__post("http://" + self.hostname + "/admin/resync")

    def fastsync(self) -> str:
        """Fastsync the Bobcat."""
        if self.dry_run:
            self.logger.warning("Dry run is enabled: Fastsync Skipped")
            return "Dry run is enabled: Normally this would show the Fastsync response"

        self.logger.info("Fastsync Bobcat")
        return self._BobcatConnection__post("http://" + self.hostname + "/admin/fastsync")
