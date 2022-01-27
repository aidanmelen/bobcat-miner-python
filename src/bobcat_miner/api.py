from __future__ import annotations
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
        # self.miner_data = {} # initialized in the BobcatConnection constructor during bobcat verification
        self.temp_data = {}
        self.speed_data = {}
        self.dig_data = {}

    def refresh_status(self) -> BobcatAPI:
        """Refresh Bobcat status data."""
        self.logger.debug("Refresh: Status Data")
        self.status_data = self._BobcatConnection__get(
            "http://" + self.hostname + "/status.json"
        ).json()

        if self.status_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_status()
        return self

    def refresh_miner(self) -> BobcatAPI:
        """Refresh Bobcat miner data."""
        self.logger.debug("Refresh: Miner Data")
        self.miner_data = self._BobcatConnection__get(
            "http://" + self.hostname + "/miner.json"
        ).json()

        if self.miner_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_miner()
        return self

    def refresh_speed(self) -> BobcatAPI:
        """Refresh Bobcat network speed data."""
        self.logger.debug("Refresh: Network Speed Data")
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
        return self

    def refresh_temp(self) -> BobcatAPI:
        """Refresh Bobcat temperature data."""
        self.logger.debug("Refresh: Temperature Data")
        self.temp_data = self._BobcatConnection__get(
            "http://" + self.hostname + "/temp.json"
        ).json()

        if self.temp_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_temp()
        return self

    def refresh_dig(self) -> BobcatAPI:
        """Refresh Bobcat DNS data."""
        self.logger.debug("Refresh Bobcat: DNS Data")
        self.dig_data = self._BobcatConnection__get("http://" + self.hostname + "/dig.json").json()

        if self.dig_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_dig()
        return self

    def refresh(
        self,
        status: bool = True,
        miner: bool = True,
        temp: bool = True,
        speed: bool = True,
        dig: bool = True,
    ) -> BobcatAPI:
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
        return self

    def reboot(self) -> None:
        """Reboot the Bobcat."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/44076
        if self.dry_run:
            self.logger.warning("Dry run is enabled: Reboot Skipped")
        else:
            self.logger.warning("Rebooting Bobcat")
            self.logger.debug(
                self._BobcatConnection__post("http://" + self.hostname + "/admin/reboot")
            )

    def reset(self) -> None:
        """Reset the Bobcat."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4412
        if self.dry_run:
            self.logger.warning("Dry run is enabled: Reset Skipped")
        else:
            self.logger.warning("Resetting Bobcat")
            self.logger.debug(
                self._BobcatConnection__post("http://" + self.hostname + "/admin/reset")
            )

    def resync(self) -> None:
        """Resync the Bobcat."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/44130
        if self.dry_run:
            self.logger.warning("Dry run is enabled: Resync Skipped")
        else:
            self.logger.warning("Resyncing Bobcat")
            self.logger.debug(
                self._BobcatConnection__post("http://" + self.hostname + "/admin/resync")
            )

    def fastsync(self) -> None:
        """Fastsync the Bobcat."""
        if self.dry_run:
            self.logger.warning("Dry run is enabled: Fastsync Skipped")
        else:
            self.logger.warning("Fastsyncing Bobcat")
            self.logger.debug(
                self._BobcatConnection__post("http://" + self.hostname + "/admin/fastsync")
            )
