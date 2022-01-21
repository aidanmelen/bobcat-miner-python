from bobcat_connection import BobcatConnection


class BobcatAPI(BobcatConnection):
    """A class for interacting with the Bobcat API endpoints."""

    def __init__(self, log_level: str = "INFO") -> None:
        super().__init__(log_level)

        self.status_data = {}
        self.miner_data = {}
        self.temp_data = {}
        self.speed_data = {}
        self.dig_data = {}

    def refresh_status(self) -> dict:
        """Refresh data for the bobcat miner status"""
        self.status_data = self.get("http://" + self.ip_address + "/status.json").json()

        if self.status_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_status()

    def refresh_miner(self) -> dict:
        """Refresh data for the bobcat miner data"""
        self.miner_data = self.get("http://" + self.ip_address + "/miner.json").json()

        if self.miner_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_miner()

    def refresh_speed(self) -> dict:
        """Refresh data for the bobcat miner network speed"""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4407606223899-Netspeed-Blockchain-Reboot
        self.speed_data = self.get("http://" + self.ip_address + "/speed.json").json()

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

    def refresh_temp(self) -> dict:
        """Refresh data for the bobcat miner temp"""
        self.temp_data = self.get("http://" + self.ip_address + "/temp.json").json()

        if self.temp_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_temp()

    def refresh_dig(self) -> dict:
        """Refresh data for the bobcat miner DNS data"""
        self.dig_data = self.get("http://" + self.ip_address + "/dig.json").json()

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
    ) -> dict:
        """Refresh data for the bobcat miner"""
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
