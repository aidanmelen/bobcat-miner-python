"""Bobcat Miner"""

from datetime import datetime

import socket
import backoff
import requests
import time


class Bobcat:
    def __init__(self, ip_address):
        self.ip_address = str(ip_address)

        self.status_data = {}
        self.miner_data = {}
        self.temp_data = {}
        self.speed_data = {}
        self.dig_data = {}

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=600,
    )
    def _get(self, url):
        """Requests get call wrapper with exponential backoff."""
        return requests.get(url)

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=600,
    )
    def _post(self, url):
        """Requests post call wrapper with exponential backoff."""
        return requests.post(url, headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"})

    def refresh_status(self):
        """Refresh data for the bobcat miner status"""
        self.status_data = self._get("http://" + self.ip_address + "/status.json").json()

    def refresh_miner(self):
        """Refresh data for the bobcat miner data"""
        self.miner_data = self._get("http://" + self.ip_address + "/miner.json").json()

    def refresh_speed(self):
        """Refresh data for the bobcat miner network speed"""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4407606223899-Netspeed-Blockchain-Reboot
        self.speed_data = self._get("http://" + self.ip_address + "/speed.json").json()

        if self.speed_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_speed()

    def refresh_temp(self):
        """Refresh data for the bobcat miner temp"""
        self.temp_data = self._get("http://" + self.ip_address + "/temp.json").json()

    def refresh_dig(self):
        """Refresh data for the bobcat miner DNS data"""
        self.dig_data = self._get("http://" + self.ip_address + "/dig.json").json()

        if self.dig_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.refresh_dig()

    def refresh(self, status=True, miner=True, temp=True, speed=True, dig=True):
        """Refresh data for the bobcat miner"""
        if speed:
            # refresh the speed endpoint first because it has a rate limit
            self.refresh_speed()
        if status:
            self.refresh_status()
        if miner:
            self.refresh_miner()
        if temp:
            self.refresh_temp()
        if dig:
            self.refresh_dig()

    @property
    def status(self):
        """Get status"""
        if not self.status_data:
            self.refresh_status()
        return self.status_data.get("status")

    @property
    def gap(self):
        """Get gap"""
        if not self.status_data:
            self.refresh_status()
        gap = self.status_data.get("gap")
        return int(gap) if gap.lstrip("-").isdigit() else 1000000000

    @property
    def miner_height(self):
        """Get miner height"""
        if not self.status_data:
            self.refresh_status()
        miner_height = self.status_data.get("miner_height")
        return int(miner_height) if miner_height.lstrip("-").isdigit() else None

    @property
    def blockchain_height(self):
        """Get blockchain height"""
        if not self.status_data:
            self.refresh_status()
        blockchain_height = self.status_data.get("blockchain_height")
        return int(blockchain_height) if blockchain_height.lstrip("-").isdigit() else None

    @property
    def epoch(self):
        """Get epoch"""
        if not self.status_data:
            self.refresh_status()
        epoch = self.status_data.get("epoch")
        return int(epoch) if epoch.lstrip("-").isdigit() else None

    @property
    def tip(self):
        """Get tip. Only available during error state"""
        if not self.status_data:
            self.refresh_status()
        return self.status_data.get("tip")

    @property
    def ota_version(self):
        """Get OTA version"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("ota_version")

    @property
    def region(self):
        """Get region"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("region")

    @property
    def frequency_plan(self):
        """Get frequency plan"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("frequency_plan")

    @property
    def animal(self):
        """Get animal"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("animal")

    @property
    def name(self):
        """Get human readable name"""
        return " ".join([word.capitalize() for word in self.animal.split("-")])

    @property
    def pubkey(self):
        """Get pubic key"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("pubkey")

    @property
    def state(self):
        """Get miner state"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("miner", {}).get("State")

    @property
    def miner_status(self):
        """Get miner status"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("miner", {}).get("Status")

    @property
    def names(self):
        """Get miner names"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("miner", {}).get("Names")

    @property
    def image(self):
        """Get miner image"""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4413004080667-Access-Diagnoser-Check-OTA-Version
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("miner", {}).get("Image")

    @property
    def created(self):
        """Get miner created"""
        if not self.miner_data:
            self.refresh_miner()
        return datetime.fromtimestamp(int(self.miner_data.get("miner", {}).get("Created")))

    @property
    def p2p_status(self):
        """Get p2p status"""
        if not self.miner_data:
            self.refresh_miner()
        return {
            x.split("|")[1].strip(): x.split("|")[2].strip()
            for x in self.miner_data.get("p2p_status", [])[3:-3]
        }

    @property
    def ports_desc(self):
        """Get port description"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("ports_desc")

    @property
    def ports(self):
        """Get ports"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("ports", {})

    @property
    def private_ip(self):
        """Get private ip"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("private_ip")

    @property
    def public_ip(self):
        """Get public ip"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("public_ip")

    @property
    def peerbook(self):
        """Get peerbook"""
        if not self.miner_data:
            self.refresh_miner()
        return "\n".join(self.miner_data.get("peerbook", []))

    @property
    def peerbook_miner(self):
        """Get the peerbook miner information"""
        if not self.miner_data:
            self.refresh_miner()

        header = self.miner_data.get("peerbook", [])[1].replace(" ", "").split("|")[1:-1]
        data = self.miner_data.get("peerbook", [])[3].replace(" ", "").split("|")[1:-1]

        return dict(zip(header, data))

    @property
    def peerbook_listen_address(self):
        """Get the peerbook listen address"""
        if not self.miner_data:
            self.refresh_miner()
        return self.miner_data.get("peerbook", [])[9].replace("|", "")

    @property
    def peerbook_peers(self):
        """Get the peerbook peer information"""
        if not self.miner_data:
            self.refresh_miner()

        header = self.miner_data.get("peerbook", [])[13].replace(" ", "").split("|")[1:-1]
        data = [
            record.replace(" ", "").split("|")[1:-1]
            for record in self.miner_data.get("peerbook", [])[15:-3]
        ]

        return [dict(zip(header, record)) for record in data]

    @property
    def timestamp(self):
        """Get timestamp"""
        if not self.miner_data:
            self.refresh_miner()
        return datetime.strptime(self.miner_data.get("timestamp"), "%Y-%m-%d %H:%M:%S %z %Z")

    @property
    def error(self):
        """Get error"""
        if not self.miner_data:
            self.refresh_miner()

        _err = self.miner_data.get("error")

        return _err if _err else None

    @property
    def temp0(self):
        """Get CPU temp sensor 0 Celsius"""
        if not self.temp_data:
            self.refresh_temp()
        return int(self.temp_data.get("temp0"))

    @property
    def temp1(self):
        """Get CPU temp sensor 1 in Celsius"""
        if not self.temp_data:
            self.refresh_temp()
        return int(self.temp_data.get("temp1"))

    @property
    def temp0_c(self):
        """Get CPU temp sensor 0 in Celsius"""
        return self.temp0

    @property
    def temp1_c(self):
        """Get CPU temp sensor 1 in Celsius"""
        return self.temp1

    @property
    def temp0_f(self):
        """Get CPU temp sensor 0 Fahrenheit"""
        return round(self.temp0 * 1.8 + 32, 1)

    @property
    def temp1_f(self):
        """Get CPU temp sensor 1 in Fahrenheit"""
        return round(self.temp1 * 1.8 + 32, 1)

    @property
    def download_speed(self):
        """Get download speed"""
        if not self.speed_data:
            self.refresh_speed()
        return self.speed_data.get("DownloadSpeed")

    @property
    def upload_speed(self):
        """Get upload speed"""
        if not self.speed_data:
            self.refresh_speed()
        return self.speed_data.get("UploadSpeed")

    @property
    def latency(self):
        """Get latency"""
        if not self.speed_data:
            self.refresh_speed()
        return self.speed_data.get("Latency")

    @property
    def dig_name(self):
        """Get dig name"""
        if not self.dig_data:
            self.refresh_dig()
        return self.dig_data.get("name")

    @property
    def dig_message(self):
        """Get dig message"""
        if not self.dig_data:
            self.refresh_dig()
        return self.dig_data.get("message")

    @property
    def dig_dns(self):
        """Get dig DNS"""
        if not self.dig_data:
            self.refresh_dig()
        return self.dig_data.get("DNS")

    @property
    def dig_records(self):
        """Get dig records"""
        if not self.dig_data:
            self.refresh_dig()
        return self.dig_data.get("records", [])

    def ping(self, timeout=5):
        """Verify network connectivity"""
        try:
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip_address, 80))
        except OSError as err:
            result = False
        else:
            result = True
        finally:
            s.close()
            return result

    def reboot(self):
        """Reboot the bobcat miner"""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4407606223899-Netspeed-Blockchain-Reboot
        self._post("http://" + self.ip_address + "/admin/reboot")

    def reset(self):
        """Reset the bobcat miner"""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4412997563931-Reset-Miner-Feature
        self._post("http://" + self.ip_address + "/admin/reset")

    def resync(self):
        """Resync the bobcat miner"""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4413004114075-Resync-Feature-
        self._post("http://" + self.ip_address + "/admin/resync")

    def fastsync(self):
        """Fastsync the bobcat miner"""
        self._post("http://" + self.ip_address + "/admin/fastsync")

    def is_bobcat(self):
        """Check if IP address is a Bobcat miner"""
        try:
            r = self._get("http://" + self.ip_address)
            return "Diagnoser - Bobcatminer Diagnostic Dashboard" in r.text
        except requests.RequestException:
            return False
