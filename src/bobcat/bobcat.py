"""Bobcat Miner"""

import backoff
import base64
import logging
import requests
import time


class Bobcat:
    def __init__(self, ip_address):
        self.ip_address = str(ip_address)

        self.status = {}
        self.miner = {}
        self.speed = {}
        self.dig = {}

        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=600,
    )
    def _requests_get(self, url):
        """Requests get call wrapper with exponential backoff annotation."""
        return requests.get(url)

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=600,
    )
    def _requests_post(self, url):
        """Requests post call wrapper with exponential backoff annotation."""
        return requests.post(url, header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"})

    def refresh_status(self):
        """Refresh data for the bobcat miner status"""
        self.status = self._requests_get("http://" + self.ip_address + "/status.json").json()
        return None

    def refresh_miner(self):
        """Refresh data for the bobcat miner data"""
        self.miner = self._requests_get("http://" + self.ip_address + "/miner.json").json()
        return None

    def refresh_speed(self):
        """Refresh data for the bobcat miner network speed"""
        self.speed = self._requests_get("http://" + self.ip_address + "/speed.json").json()
        return None

    def refresh_dig(self):
        """Refresh data for the bobcat miner DNS data"""
        self.dig = self._requests_get("http://" + self.ip_address + "/dig.json").json()
        return None

    def refresh(self, status=True, miner=True, speed=True, dig=True):
        """Refresh data for the bobcat miner"""
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
        """Resync the bobcat miner"""
        return self._requests_post("http://" + self.ip_address + "/admin/resync")

    def reset(self):
        """Reset the bobcat miner"""
        return self._requests_post("http://" + self.ip_address + "/admin/reset")

    def reboot(self):
        """Reboot the bobcat miner"""
        return self._requests_post("http://" + self.ip_address + "/admin/reboot")

    def fastsync(self):
        """Fastsync the bobcat miner"""
        return self._requests_post("http://" + self.ip_address + "/admin/fastsync")

    def can_connect(self):
        """Check local connection to the bobcat miner API"""
        try:
            return requests.get("http://" + self.ip_address).ok
        except requests.ConnectionError:
            return False

    def is_running(self):
        """Check if the bobcat miner is running"""
        return self.miner.get("miner", {}).get("State").lower() == "running"

    def is_synced(self):
        """Check if the bobcat miner is synced with the Helium blockchain"""
        return self.status.get("status").lower() == "synced"

    def is_temp_safe(self):
        """Check if the bobcat miner is operating within a safe tempurature range"""
        temp0 = int(self.miner.get("temp0").strip(" °C"))
        temp1 = int(self.miner.get("temp1").strip(" °C"))

        # https://www.bobcatminer.com/post/bobcat-diagnoser-user-guide
        return temp0 >= 0 and temp0 < 65 and temp1 >= 0 and temp1 < 65

    def has_errors(self):
        """Check for bobcat errors"""
        has_error = self.miner["errors"] != ""
        has_miner_state_error = "error" in self.miner["miner"]["State"].lower()
        has_miner_status_error = "error" in self.miner["miner"]["Status"].lower()
        has_p2p_status_error = any(["error" in h.lower() for h in self.miner["p2p_status"]])
        has_epoch_error = "error" in self.miner["epoch"]
        has_height_error = any(["error" in h.lower() for h in self.miner["height"]])
        has_peerbook_error = any(["error" in h.lower() for h in self.miner["peerbook"]])

        return (
            has_error
            or has_miner_state_error
            or has_miner_status_error
            or has_p2p_status_error
            or has_epoch_error
            or has_height_error
            or has_peerbook_error
        )

    def is_healthy(self):
        """Check if the is synced with the Helium blockchain"""
        return (
            self.is_running() and self.is_synced() and self.is_temp_safe() and not self.has_errors()
        )

    def is_relayed(self):
        """Check if the bobcat is being relayed"""

        # If the listen_addrs is via tcp/44158, it means your hotspot is not relayed.
        # A relayed hotspot's listen address will be via another hotspot on the network
        public_ip = self.miner.get("public_ip")
        port_44158_is_open = any(
            [f"/ip4/{public_ip}/tcp/44158" in pb.lower() for pb in self.miner.get("peerbook", [])]
        )
        return not port_44158_is_open

    def is_local_network_slow(self):
        """Check if the local network for slowness and latency"""
        download_speed = int(self.speed.get("DownloadSpeed").strip(" Mbit/s"))
        upload_speed = int(self.speed.get("UploadSpeed").strip(" Mbit/s"))
        latency = int(self.speed.get("Latency").strip("ms"))

        is_download_speed_slow = download_speed < 5
        is_upload_speed_slow = upload_speed < 5
        is_latency_high = latency > 50

        return any(is_download_speed_slow, is_upload_speed_slow, is_latency_high)

    def should_fastsync(self):
        """Check if the bobcat miner needs a fastsync"""
        try:
            gap = int(self.status["gap"])
        except:
            # fastsync will not fix an unhealthy miner
            return False
        return gap > 400 and gap < 10000

    def should_resync(self):
        """Check if the bobcat miner needs a resync"""
        try:
            gap = int(self.status["gap"])
        except:
            # resync may fix unhealthy miner
            return True
        return gap >= 10000

    def should_reboot(self):
        """Check if the bobcat miner needs to be reboot"""
        try:
            gap = int(self.status["gap"])
        except:
            # reboot may fix unhealthy miner
            return True
        return not self.has_errors() and gap <= 10000

    def should_reset(self):
        """Check if the bobcat miner needs to be reset"""
        try:
            gap = int(self.status["gap"])
        except:
            # reset may fix unhealthy miner
            return True
        return self.has_errors() and gap > 10000

    def autopilot(self):
        """Diagnose the Bobcat miner and ensure it is healthy"""

        logging.info("running autopilot...")

        if not self.can_connect():
            logging.error(
                f"Failed to connect to bobcat at {self.ip_address}. Please check your router for the bobcat's private ip address."
            )
            return None

        if not self.status:
            logging.info("refresh status data")
            self.refresh_status()

        if not self.miner:
            logging.info("refresh miner data")
            self.refresh_miner()

        if self.is_healthy:
            logging.info("bobcat is healthy")

        else:
            logging.info("bobcat is unhealthy")

            # Try REBOOT, if not work, try RESET (wait for 30 minutes) -> FAST SYNC  (wait for 30 minutes).

            if self.should_reboot():
                logging.info("bobcat rebooting...")
                self.reboot()

            logging.info("refresh status data")
            self.refresh_status()

            logging.info("refresh miner data")
            self.refresh_miner()

            if self.should_reset():
                logging.info("bobcat is still unhealthy after reboot")
                logging.info("bobcat resetting...")
                self.reset()

                logging.info("waiting for 30 minutes...")
                time.sleep(1800)

                logging.info("refresh status data")
                self.refresh_status()

                while self.should_fastsync():

                    logging.info("bobcat fastsync...")
                    self.fastsync()

                    logging.info("waiting for 30 minutes...")
                    time.sleep(1800)

        return None
