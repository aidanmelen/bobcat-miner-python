"""Bobcat Autopilot"""

import logging
import json
import time

from filelock import Timeout, FileLock

try:
    from .bobcat import Bobcat
except:
    from bobcat import Bobcat

try:
    from .helpers import get_logger
except:
    from helpers import get_logger


class Autopilot:

    ONE_MINUTE = 60
    FIVE_MINUTES = 300
    TEN_MINUTES = 600
    THIRTY_MINUTES = 1800

    def __init__(
        self,
        bobcat,
        log_file="/var/log/bobcat-autopilot.log",
        log_level=logging.DEBUG,
        dry_run=False,
    ):
        assert isinstance(bobcat, Bobcat)
        self.bobcat = bobcat
        self.logger = get_logger(log_file, log_level)
        self.dry_run = dry_run

        return None

    def diagnose_relay(self):
        """Diagnose the Bobcat's relay"""

        self.logger.debug("Diagnosing the Bobcat's relay")

        listen_address = self.bobcat.peerbook_listen_address
        is_port_44158_open = f"/ip4/{self.bobcat.public_ip}/tcp/44158" in listen_address

        is_relayed = not is_port_44158_open and self.bobcat.p2p_status.get("nat_type") != "none"

        if is_relayed:
            self.logger.warning(f"The Bobcat is relayed via {listen_address}")
            self.logger.debug(
                "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4413699764763-Confirming-Relay-Status-in-Diagnoser"
            )
        else:
            self.logger.info(f"The Bobcat is not relayed")

        return is_relayed

    def diagnose_temp(self):
        """Diagnosing the Bobcat's CPU tempurature"""

        self.logger.debug("Diagnosing the Bobcat's CPU tempurature")

        is_too_cold = self.bobcat.temp0 < 0 or self.bobcat.temp1 < 0
        is_hot_warning = (self.bobcat.temp0 >= 65 and self.bobcat.temp0 < 70) or (
            self.bobcat.temp1 >= 65 and self.bobcat.temp1 < 70
        )
        is_hot_error = self.bobcat.temp0 >= 70 or self.bobcat.temp1 >= 70

        if is_too_cold:
            self.logger.warning("The Bobcat is too cold ⛄")

        if is_hot_warning:
            self.logger.warning("The Bobcat is getting hot 🔥")

        if is_hot_error:
            self.logger.error("The Bobcat is too hot 🔥")

        is_temp_safe = not (is_too_cold and (is_hot_warning or is_hot_error))

        if not is_temp_safe:
            self.logger.debug(
                "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4407605756059-Sync-Status-Temp-Monitoring"
            )
        else:
            self.logger.info("The Bobcat's CPU tempurature is good")

        return is_temp_safe

    def diagnose_network_speed(self):
        """Diagnose the Bobcat's network speed"""

        self.logger.debug("Diagnosing the Bobcat's network speed")

        download_speed = int(self.bobcat.download_speed.strip(" Mbit/s"))
        upload_speed = int(self.bobcat.upload_speed.strip(" Mbit/s"))
        latency = float(self.bobcat.latency.strip("ms"))

        is_download_speed_slow = download_speed < 5
        is_upload_speed_slow = upload_speed < 5
        is_latency_high = latency > 50

        if is_download_speed_slow:
            self.logger.warning(
                f"The Bobcat's download speed is slow: {self.bobcat.download_speed}"
            )

        if is_upload_speed_slow:
            self.logger.warning(f"The Bobcat's upload speed is slow: {self.bobcat.upload_speed}")

        if is_latency_high:
            self.logger.warning(f"The Bobcat's lag is high: {self.bobcat.latency}")

        is_network_speed_slow = any([is_download_speed_slow, is_upload_speed_slow, is_latency_high])

        if is_network_speed_slow:
            self.logger.debug(
                "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4409231342363-Miner-is-Offline"
            )
        else:
            self.logger.info("the Bobcat's network speed is good")

        return is_network_speed_slow

    def ping(self, backoff_time=FIVE_MINUTES, max_attempts=3):
        """Ping the Bobcat until it connects or attempts are maxed out."""

        if self.dry_run:
            backoff_time = 1

        self.logger.debug(f"Ping the Bobcat ({self.bobcat.ip_address})")

        attempt_count = 0
        while not self.bobcat.ping() and (attempt_count < max_attempts):

            self.logger.debug("The Bobcat is unreachable")

            self.logger.debug(f"Waiting {int(backoff_time / 60)} Minutes ⏳")
            time.sleep(backoff_time)

            attempt_count += 1

        if attempt_count >= max_attempts:
            self.logger.critical(f"The Bobcat is unreachable after {max_attempts} attempts.")
            return False

        self.logger.debug("Successfully connected to the Bobcat")
        return True

    def wait_loading(self, wait_time=THIRTY_MINUTES, backoff_time=FIVE_MINUTES, max_attempts=10):
        """Wait for bobcat when loading"""

        if self.dry_run:
            wait_time = 1

        self.bobcat.refresh_status()

        attempt_count = 0
        while self.bobcat.status.upper() == "LOADING" and (attempt_count < max_attempts):

            self.logger.info("The Bobcat is loading")

            self.logger.debug(f"Waiting {int(backoff_time / 60)} Minutes ⏳")
            time.sleep(backoff_time)

            attempt_count += 1

        return None

    def wait(self, wait_time=THIRTY_MINUTES, backoff_time=FIVE_MINUTES):
        """Wait for bobcat"""

        if self.dry_run:
            wait_time = 1

        self.logger.debug(f"Waiting {int(wait_time / 60)} Minutes ⏳")
        time.sleep(wait_time)

        self.ping()

        self.wait_loading(wait_time, backoff_time)

        return None

    def reboot(self):
        """Autopilot manages the bobcat reboot"""

        self.logger.debug("Rebooting the Bobcat")

        if not self.dry_run:
            self.bobcat.reboot()
            self.wait()

        self.logger.debug("Finished rebooting the Bobcat")

    def reset(self, max_attempts=3):
        """Autopilot manages the bobcat reset"""

        self.logger.debug("Resetting the Bobcat")

        attempt_count = 0
        while (self.bobcat.status.upper() in ["ERROR", "DOWN"]) and (attempt_count < max_attempts):

            if not self.dry_run:
                self.bobcat.reset()
                self.wait()

            attempt_count += 1

        self.logger.debug("Finished resetting the Bobcat")

    def resync(self):
        """Autopilot manages the bobcat resync"""

        self.logger.debug("Resyncing the Bobcat")

        self.bobcat.refresh_status()

        if not self.dry_run:
            self.bobcat.resync()
            self.wait()

        self.logger.debug("Finished resyncing the Bobcat")

        return None

    def fastsync(self):
        """Autopilot manages the bobcat fastsync"""

        if self.bobcat.gap < 400:
            self.logger.debug(
                f"Cancelling the fastsync. The blockchain gap ({self.bobcat.gap}) is less than 400."
            )
            return None

        if self.bobcat.status.upper() in ["ERROR", "DOWN"] or self.bobcat.error:
            self.logger.debug(
                f"Cancelling the fastsync because fastsync only works on a healthly Bobcat"
            )
            return None

        self.logger.debug("Fastsyncing the Bobcat")

        max_attempts = 5
        attempt_count = 0

        while self.bobcat.gap > 400 and (attempt_count < max_attempts):

            if not self.dry_run:
                self.bobcat.fastsync()
                self.wait()

            self.bobcat.refresh_status()

            attempt_count += 1

        self.logger.debug("Finished fastsyncing the Bobcat")

        return None

    def is_syncing(self, poll_rate=TEN_MINUTES, poll_total=6):
        """Poll the Bobcat's gap to see if it is syncing over time"""
        if poll_total < 2:
            self.logger.warning(
                "Not polling the Bobcat's blockchain gap because the poll_total is too small"
            )
            return False

        gap_polls = []

        self.logger.debug("Start polling the Bobcat's blockchain gap")

        for _ in range(poll_total):
            self.bobcat.refresh_status()
            gap = self.bobcat.gap
            gap_polls.append(gap)

            self.logger.debug(f"Polled gap: {gap}")

            self.logger.debug(f"Waiting {int(wait_time / 60)} Minutes ⏳")
            if self.dry_run:
                time.sleep(1)
            else:
                time.sleep(poll_rate)

        self.logger.debug("Finished polling the Bobcat's blockchain gap")

        previous_gap = gap_polls[0]
        gap_growth_count = 0

        for gap in gap_polls[1:]:
            if gap > previous_gap:
                gap_growth_count += 1
                previous_gap = gap

        is_gap_growing = gap_growth_count > poll_total / 2

        if is_gap_growing:
            self.logger.error("The Bobcat is not syncing")
            return False
        else:
            self.logger.debug("Leave the Bobcat alone because it syncing")
            return True

    def catch_up(self):
        """Catch the Bobcat to the top of the blockchain"""
        self.logger.warning("Attempt to sync the Bobcat")

        if self.is_syncing():
            return None

        self.reboot()
        self.bobcat.refresh_status()

        if self.is_syncing():
            return None

        self.logger.info("The reboot did not fix the Bobcat's syncing issue")
        if self.bobcat.gap > 400:
            self.fastsync()

        if not self.is_syncing():
            self.logger.error("The reboot failed to sync the Bobcat")

        return None

    def run(self):
        """Diagnose and repair bobcat"""

        self.logger.debug("The Bobcat Autopilot is starting")
        self.logger.warning("Do not unplug power to the Bobcat miner")

        try:
            lock = FileLock("/tmp/bobcat-autopilot", timeout=1)

            with lock:

                if not self.ping():
                    self.logger.critical(
                        "Cancelling Bobcat Autopilot. Please double check the IP address and network and try again."
                    )
                    return None

                self.logger.debug("Refreshing Bobcat data")
                self.bobcat.refresh()

                if self.bobcat.status.upper() in ["ERROR", "DOWN"]:

                    self.logger.error("The Bobcat is down")
                    self.logger.debug(
                        "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4413666097051-Status-Down-4413666097051-Status-Down-"
                    )

                    if self.bobcat.tip:
                        self.logger.debug(f"tip: {self.bobcat.tip}")

                    self.reboot()
                    self.reset()
                    self.fastsync()

                if self.bobcat.status.upper() == "HEIGHT API ERROR":

                    self.logger.error("The Bobcat is down")
                    self.logger.debug(
                        "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4413699665435-API-Error"
                    )

                    if self.bobcat.tip:
                        self.logger.debug(f"tip: {self.bobcat.tip}")

                    self.reboot()
                    self.reset()
                    self.fastsync()

                if self.bobcat.gap > 400:

                    self.logger.error("The Bobcat is not synced")
                    self.logger.debug(
                        "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4414476039451-Syncing-Issues"
                    )

                    self.catch_up()

                # Diagnose
                self.diagnose_relay()
                self.diagnose_temp()
                self.diagnose_network_speed()

        except Timeout:
            self.logger.warning("Stopping. Another instance of bobcat-autopilot currently running")
        except Exception as err:
            self.logger.critical(f"Encountered unexpected error: {str(err)}")

        self.logger.debug("The Bobcat Autopilot is finished 🏁")
        return None
