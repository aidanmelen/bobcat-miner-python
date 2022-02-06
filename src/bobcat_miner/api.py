from __future__ import annotations
from typing import List
from requests import Response

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
        """Refresh Bobcat status data.
        Returns:
            (BobcatAPI): The instance of the BobcatAPI.
        """
        self._status_data = self._BobcatConnection__get(
            "http://" + self._hostname + "/status.json"
        ).json()

        if self._trace:
            self.logger.debug(
                "Refresh: Status Data",
                extra={"description": f"\n```\n{json.dumps(self._status_data, indent=4)}\n```"},
            )
        else:
            self.logger.debug("Refresh: Status Data")

        if self._status_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_status()
        return self

    def refresh_miner(self) -> BobcatAPI:
        """Refresh Bobcat miner data.
        Returns:
            (BobcatAPI): The instance of the BobcatAPI.
        """

        self._BobcatConnection__refresh_miner()

        return self

    def refresh_speed(self) -> BobcatAPI:
        """Refresh Bobcat network speed data.
        Returns:
            (BobcatAPI): The instance of the BobcatAPI.
        """
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4407606223899-Netspeed-Blockchain-Reboot
        self._speed_data = self._BobcatConnection__get(
            "http://" + self._hostname + "/speed.json"
        ).json()

        if self._trace:
            self.logger.debug(
                "Refresh: Network Speed Data",
                extra={"description": f"\n```\n{json.dumps(self._speed_data, indent=4)}\n```"},
            )
        else:
            self.logger.debug("Refresh: Network Speed Data")

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
        """Refresh Bobcat temperature data.
        Returns:
            (BobcatAPI): The instance of the BobcatAPI.
        """
        self._temp_data = self._BobcatConnection__get(
            "http://" + self._hostname + "/temp.json"
        ).json()

        if self._trace:
            self.logger.debug(
                "Refresh: Temperature Data",
                extra={"description": f"\n```\n{json.dumps(self._temp_data, indent=4)}\n```"},
            )
        else:
            self.logger.debug("Refresh: Temperature Data")

        if self._temp_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_temp()
        return self

    def refresh_dig(self) -> BobcatAPI:
        """Refresh Bobcat DNS data.
        Returns:
            (BobcatAPI): The instance of the BobcatAPI.
        """
        self._dig_data = self._BobcatConnection__get(
            "http://" + self._hostname + "/dig.json"
        ).json()

        if self._trace:
            self.logger.debug(
                "Refresh: DNS Data",
                extra={"description": f"\n```\n{json.dumps(self._dig_data, indent=4)}\n```"},
            )
        else:
            self.logger.debug("Refresh: DNS Data")

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
        """Refresh data for the Bobcat.
        Args:
            status (bool): Whether to refresh the Bobcat status data.
            miner (bool): Whether to refresh the Bobcat miner data.
            temp (bool): Whether to refresh the Bobcat temperature data.
            speed (bool): Whether to refresh the Bobcat network speed data.
            dig (bool): Whether to refresh the Bobcat DNS data.
        Returns:
            (BobcatAPI): The instance of the BobcatAPI.
        """
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

    def __reboot(self) -> Response:
        """Reboot the Bobcat.
        Returns:
            (str): The response.
        """
        # https://bobcatminer.zendesk.com/hc/en-us/articles/44076
        self.logger.warning("Rebooting Bobcat")
        return self._BobcatConnection__post("http://" + self._hostname + "/admin/reboot")

    def __reset(self) -> Response:
        """Reset the Bobcat.
        Returns:
            (str): The response.
        """
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4412
        self.logger.warning("Resetting Bobcat")
        return self._BobcatConnection__post("http://" + self._hostname + "/admin/reset")

    def __resync(self) -> Response:
        """Resync the Bobcat.
        Returns:
            (Response): The response.
        """
        # https://bobcatminer.zendesk.com/hc/en-us/articles/44130
        self.logger.warning("Resyncing Bobcat")
        return self._BobcatConnection__post("http://" + self._hostname + "/admin/resync")

    def __fastsync(self) -> Response:
        """Fastsync the Bobcat.
        Returns:
            (str): The response.
        """
        self.logger.warning("Fastsyncing Bobcat")
        return self._BobcatConnection__post("http://" + self._hostname + "/admin/fastsync")
