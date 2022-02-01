from __future__ import annotations
from bs4 import BeautifulSoup
from typing import List

import json
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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def refresh_status(self) -> BobcatAPI:
        """Refresh Bobcat status data."""
        self._status_data = self._BobcatConnection__get(
            "http://" + self._hostname + "/status.json"
        ).json()

        if self._trace:
            self._logger.debug(
                "Refresh: Status Data",
                extra={"description": f"\n```\n{json.dumps(self._status_data, indent=4)}\n```"},
            )
        else:
            self._logger.debug("Refresh: Status Data")

        if self._status_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_status()
        return self

    def refresh_miner(self) -> BobcatAPI:
        """Refresh Bobcat miner data."""
        self._miner_data = self._BobcatConnection__get(
            "http://" + self._hostname + "/miner.json"
        ).json()

        if self._trace:
            self._logger.debug(
                "Refresh: Miner Data",
                extra={"description": f"{json.dumps(self._miner_data, indent=4)}"},
            )
        else:
            self._logger.debug("Refresh: Miner Data")

        if self._miner_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_miner()
        return self

    def refresh_speed(self) -> BobcatAPI:
        """Refresh Bobcat network speed data."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4407606223899-Netspeed-Blockchain-Reboot
        self._speed_data = self._BobcatConnection__get(
            "http://" + self._hostname + "/speed.json"
        ).json()

        if self._trace:
            self._logger.debug(
                "Refresh: Network Speed Data",
                extra={"description": f"\n```\n{json.dumps(self._speed_data, indent=4)}\n```"},
            )
        else:
            self._logger.debug("Refresh: Network Speed Data")

        if (self._speed_data == {"message": "rate limit exceeded"}) or (
            self._speed_data
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
        self._temp_data = self._BobcatConnection__get(
            "http://" + self._hostname + "/temp.json"
        ).json()

        if self._trace:
            self._logger.debug(
                "Refresh: Temperature Data",
                extra={"description": f"\n```\n{json.dumps(self._temp_data, indent=4)}\n```"},
            )
        else:
            self._logger.debug("Refresh: Temperature Data")

        if self._temp_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_temp()
        return self

    def refresh_dig(self) -> BobcatAPI:
        """Refresh Bobcat DNS data."""
        self._dig_data = self._BobcatConnection__get(
            "http://" + self._hostname + "/dig.json"
        ).json()

        if self._trace:
            self._logger.debug(
                "Refresh: DNS Data",
                extra={"description": f"\n```\n{json.dumps(self._dig_data, indent=4)}\n```"},
            )
        else:
            self._logger.debug("Refresh: DNS Data")

        if self._dig_data == {"message": "rate limit exceeded"}:
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

    def reboot(self) -> str:
        """Reboot the Bobcat."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/44076
        if self._dry_run:
            self._logger.warning("Dry run is enabled: Reboot Skipped")
        else:
            self._logger.warning("Rebooting Bobcat")
            resp = self._BobcatConnection__post("http://" + self._hostname + "/admin/reboot")
            return self.__parse_html(resp.text)

    def reset(self) -> str:
        """Reset the Bobcat."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4412
        if self._dry_run:
            self._logger.warning("Dry run is enabled: Reset Skipped")
        else:
            self._logger.warning("Resetting Bobcat")
            resp = self._BobcatConnection__post("http://" + self._hostname + "/admin/reset")
            return self.__parse_html(resp.text)

    def resync(self) -> str:
        """Resync the Bobcat."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/44130
        if self._dry_run:
            self._logger.warning("Dry run is enabled: Resync Skipped")
        else:
            self._logger.warning("Resyncing Bobcat")
            resp = self._BobcatConnection__post("http://" + self._hostname + "/admin/resync")
            return self.__parse_html(resp.text)

    def fastsync(self) -> str:
        """Fastsync the Bobcat."""
        if self._dry_run:
            self._logger.warning("Dry run is enabled: Fastsync Skipped")
        else:
            self._logger.warning("Fastsyncing Bobcat")
            resp = self._BobcatConnection__post("http://" + self._hostname + "/admin/fastsync")
            return self.__parse_html(resp.text)

    def __parse_html(self, html) -> str:
        """Parse HTML and return a str

        Args:
            html (str): The HTML to be parsed.
        """
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n")
