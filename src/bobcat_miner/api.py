try:
    from connection import BobcatConnection
except:
    from .connection import BobcatConnection


class BobcatAPI(BobcatConnection):
    """A class for interacting with the Bobcat API endpoints."""

    def __init__(self, ip_address: str = None, dry_run: bool = False, logger: str = None) -> None:
        super().__init__(ip_address, logger)

        self.dry_run = dry_run

        self.status_data = {}
        self.miner_data = {}
        self.temp_data = {}
        self.speed_data = {}
        self.dig_data = {}

    def refresh_status(self) -> None:
        """Refresh data for the Bobcat status"""
        self.status_data = self._BobcatConnection__get(
            "http://" + self.ip_address + "/status.json"
        ).json()

        if self.status_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_status()

    def refresh_miner(self) -> None:
        """Refresh data for the Bobcat data."""
        self.miner_data = self._BobcatConnection__get(
            "http://" + self.ip_address + "/miner.json"
        ).json()

        if self.miner_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_miner()

    def refresh_speed(self) -> None:
        """Refresh data for the Bobcat network speed."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4407606223899-Netspeed-Blockchain-Reboot
        self.speed_data = self._BobcatConnection__get(
            "http://" + self.ip_address + "/speed.json"
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
        """Refresh data for the Bobcat temp."""
        self.temp_data = self._BobcatConnection__get(
            "http://" + self.ip_address + "/temp.json"
        ).json()

        if self.temp_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_temp()

    def refresh_dig(self) -> None:
        """Refresh data for the Bobcat DNS data."""
        self.dig_data = self._BobcatConnection__get(
            "http://" + self.ip_address + "/dig.json"
        ).json()

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
            self.logger.warning("Skipping (reboot) because this is a dry run")
            return None

        return self._BobcatConnection__post("http://" + self.ip_address + "/admin/reboot")

    def reset(self) -> str:
        """Reset the Bobcat."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4412997563931-Reset-Miner-Feature
        if self.dry_run:
            self.logger.warning("Skipping (reset) because this is a dry run")
            return None

        return self._BobcatConnection__post("http://" + self.ip_address + "/admin/reset")

    def resync(self) -> str:
        """Resync the Bobcat."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4413004114075-Resync-Feature-
        if self.dry_run:
            self.logger.warning("Skipping (resync) because this is a dry run")
            return None

        return self._BobcatConnection__post("http://" + self.ip_address + "/admin/resync")

    def fastsync(self) -> str:
        """Fastsync the Bobcat."""
        if self.dry_run:
            self.logger.warning("Skipping (fastsync) because this is a dry run")
            return None

        return self._BobcatConnection__post("http://" + self.ip_address + "/admin/fastsync")
