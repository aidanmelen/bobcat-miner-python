"""Bobcat Miner"""

from datetime import datetime

import socket
import backoff
import requests


class Bobcat:
    def __init__(self, ip_address):
        self.ip_address = str(ip_address)

        self.status_data = {}
        self.miner_data = {}
        self.temp_data = {}
        self.speed_data = {}
        self.dig_data = {}

    def ping(self):
        """Verify connectivity"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock.connect_ex((self.ip_address, 80))

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=600,
    )
    def _get(self, url):
        """Requests get call wrapper with exponential backoff."""
        return requests.get(url).json()

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=600,
    )
    def _post(self, url):
        """Requests post call wrapper with exponential backoff."""
        return requests.post(url, header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"})

    def refresh_status(self):
        """Refresh data for the bobcat miner status"""
        self.status_data = self._get("http://" + self.ip_address + "/status.json")
        return None

    def refresh_miner(self):
        """Refresh data for the bobcat miner data"""
        self.miner_data = self._get("http://" + self.ip_address + "/miner.json")
        return None

    def refresh_speed(self):
        """Refresh data for the bobcat miner network speed"""
        self.speed_data = self._get("http://" + self.ip_address + "/speed.json")
        return None

    def refresh_temp(self):
        """Refresh data for the bobcat miner temp"""
        self.temp_data = self._get("http://" + self.ip_address + "/temp.json")
        return None

    def refresh_dig(self):
        """Refresh data for the bobcat miner DNS data"""
        self.dig_data = self._get("http://" + self.ip_address + "/dig.json")
        return None

    def refresh(self, status=True, miner=True, temp=True, speed=True, dig=True):
        """Refresh data for the bobcat miner"""
        if status:
            self.refresh_status()
        if miner:
            self.refresh_miner()
        if temp:
            self.refresh_temp()
        if speed:
            self.refresh_speed()
        if dig:
            self.refresh_dig()
        return None

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
        return int(self.status_data.get("gap"))

    @property
    def miner_height(self):
        """Get miner height"""
        if not self.status_data:
            self.refresh_status()
        return int(self.status_data.get("miner_height"))

    @property
    def blockchain_height(self):
        """Get blockchain height"""
        if not self.status_data:
            self.refresh_status()
        return int(self.status_data.get("blockchain_height"))

    @property
    def epoch(self):
        """Get epoch"""
        if not self.status_data:
            self.refresh_status()
        return int(self.status_data.get("epoch"))

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
        return self.miner_data.get("peerbook", [])

    @property
    def listen_address(self):
        """Get listen address"""
        for i, e in enumerate(self.peerbook):
            if "listen_addrs" in e:
                return self.peerbook[i + 2].strip("|").strip()
        else:
            return None

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

    @property
    def is_running(self):
        """Check if the bobcat miner is running"""
        return self.state.lower() == "running"

    @property
    def is_synced(self):
        """Check if the bobcat miner is synced with the Helium blockchain"""
        return self.status.lower() == "synced"

    @property
    def is_loading(self):
        """Check if the bobcat miner is loading"""
        return self.status.lower() == "loading"

    @property
    def is_relayed(self):
        """Check if the bobcat is being relayed"""

        # If the listen_addrs is via tcp/44158, it means your hotspot is not relayed.
        # A relayed hotspot's listen address will be via another hotspot on the network
        is_port_44158_open = self.public_ip in self.listen_address

        return not is_port_44158_open and self.p2p_status.get("nat_type") == "none"

    @property
    def is_temp_safe(self):
        """Check for bobcat CPU tempurature outside the normal operating tempurature range."""
        # https://www.bobcatminer.com/post/bobcat-diagnoser-user-guide
        return self.temp0 >= 0 and self.temp0 < 65 and self.temp1 >= 0 and self.temp1 < 65

    @property
    def is_local_network_slow(self):
        """Check for slowness and latency on the local network"""
        download_speed = int(self.download_speed.strip(" Mbit/s"))
        upload_speed = int(self.upload_speed.strip(" Mbit/s"))
        latency = float(self.latency.strip("ms"))

        is_download_speed_slow = download_speed < 5
        is_upload_speed_slow = upload_speed < 5
        is_latency_high = latency > 50

        return any([is_download_speed_slow, is_upload_speed_slow, is_latency_high])

    def reboot(self):
        """Reboot the bobcat miner"""
        return self._post("http://" + self.ip_address + "/admin/reboot")

    def reset(self):
        """Reset the bobcat miner"""
        return self._post("http://" + self.ip_address + "/admin/reset")

    def resync(self):
        """Resync the bobcat miner"""
        return self._post("http://" + self.ip_address + "/admin/resync")

    def fastsync(self):
        """Fastsync the bobcat miner"""
        return self._post("http://" + self.ip_address + "/admin/fastsync")
