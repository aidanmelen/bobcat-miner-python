"""Bobcat Autopilot"""

import logging
import json
import time

from filelock import Timeout, FileLock

try:
    from .bobcat import Bobcat
except:
    from bobcat import Bobcat


ONE_MINUTE = 60
FIVE_MINUTES = 300
TEN_MINUTES = 600
THIRTY_MINUTES = 1800


class Autopilot:
    def __init__(self, bobcat):
        assert isinstance(bobcat, Bobcat)
        self.bobcat = bobcat
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    @property
    def is_relayed(self):
        """Check for bobcat relay"""

        # https://bobcatminer.zendesk.com/hc/en-us/articles/4407611835163-Miner-5s-Miner-Slow-Down-

        listen_address = self.bobcat.peerbook[1]
        is_port_44158_open = f"/ip4/{self.bobcat.public_ip}/tcp/44158" in listen_address
        return not is_port_44158_open and self.bobcat.p2p_status.get("nat_type") != "none"

    @property
    def is_temp_safe(self):
        """Check for bobcat CPU tempurature outside the normal operating tempurature range."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4407605756059-Sync-Status-Temp-Monitoring
        return (
            self.bobcat.temp0 >= 0
            and self.bobcat.temp0 < 70
            and self.bobcat.temp1 >= 0
            and self.bobcat.temp1 < 70
        )

    @property
    def is_local_network_slow(self):
        """Check for slowness and latency on the local network"""
        download_speed = int(self.bobcat.download_speed.strip(" Mbit/s"))
        upload_speed = int(self.bobcat.upload_speed.strip(" Mbit/s"))
        latency = float(self.bobcat.latency.strip("ms"))

        is_download_speed_slow = download_speed < 5
        is_upload_speed_slow = upload_speed < 5
        is_latency_high = latency > 50

        return any([is_download_speed_slow, is_upload_speed_slow, is_latency_high])

    @property
    def is_gap_growing(self):
        """Poll the gap and return whether the blockchain gap is growing or not"""

        poll_rate = TEN_MINUTES
        poll_total = 6

        # start polling the gap
        gap_polls = []

        for _ in range(poll_total):
            self.bobcat.refresh_status()
            gap_polls.append(self.bobcat.gap)
            print(gap_polls)
            time.sleep(poll_rate)

        # count occurences of growing gap
        previous_gap = gap_polls[0]
        gap_growth_count = 0

        for gap in gap_polls[1:]:
            if gap > previous_gap:
                gap_growth_count += 1
                previous_gap = gap

        return gap_growth_count > poll_total / 2

    def wait(self):
        """Wait for bobcat"""
        time.sleep(FIVE_MINUTES)

        while not self.bobcat.ping():
            time.sleep(ONE_MINUTE)

        return None

    def reboot_reset_fastsync(self):
        """First Try Reboot -> Then Try Reset -> Then Try Fastsync"""

        # First Try Reboot
        self.bobcat.reboot()
        self.wait()

        if self.bobcat.status.upper() not in ["ERROR", "DOWN"]:

            # The reboot fixed the bobcat
            return None

        # Then Try Reset
        max_attempts = 5
        attempt_count = 0
        while (self.bobcat.status.upper() in ["ERROR", "DOWN"]) and (attempt_count < max_attempts):
            self.bobcat.reset()
            self.wait()

        # Then Try Fastsync
        max_attempts = 5
        attempt_count = 0
        while self.bobcat.gap > 400 and (attempt_count < max_attempts):
            self.bobcat.fastsync()
            fastsync_attempt_count += 1
            self.wait()

        else:
            if self.is_gap_growing():
                self.bobcat.is_local_network_slow()
                # TODO

    def run(self):
        """Diagnose and repair bobcat"""
        try:
            lock = FileLock("/tmp/bobcat-autopilot", timeout=1)

            with lock:
                if self.bobcat.status.upper() in ["ERROR", "DOWN"]:
                    # https://bobcatminer.zendesk.com/hc/en-us/articles/4413666097051-Status-Down-4413666097051-Status-Down-
                    self.reboot_reset_fastsync()

                if self.bobcat.status.upper() == "HEIGHT API ERROR":
                    # https://bobcatminer.zendesk.com/hc/en-us/articles/4413699665435-API-Error
                    self.reboot_reset_fastsync()

                if self.bobcat.status.upper() == "SYNCING":
                    if self.is_gap_growing():
                        self.bobcat.is_local_network_slow()

        except Timeout:
            logging.warn("Do nothing. Another instance of bobcat-autopilot currently running.")
