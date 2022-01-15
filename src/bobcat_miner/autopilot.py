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


class BobcatConnectionError(Exception):
    """Error for when the Bobcat miner is unreachable"""

    pass


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
            self.logger.info(f"The Bobcat is not relayed 💰")

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
            self.logger.error("The Bobcat is too cold ⛄")

        if is_hot_warning:
            self.logger.warning("The Bobcat is getting hot 🔥")

        if is_hot_error:
            self.logger.error("The Bobcat is too hot 🔥")

        is_temp_dangerous = not (is_too_cold and (is_hot_warning or is_hot_error))

        if is_temp_dangerous:
            self.logger.debug(
                "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4407605756059-Sync-Status-Temp-Monitoring"
            )
        else:
            self.logger.info("The Bobcat's CPU tempurature is good")

        return is_temp_dangerous

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
            self.logger.warning(
                "Connecting the Bobcat to the internet over wifi can cause syncing issue resulting in reduce earnings"
            )
            self.logger.debug(
                "Connecting the Bobcat to the internet with a hard wired ethernet cable will reduce syncing issues and will maximize earning potential"
            )
            self.logger.debug(
                "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4409231342363-Miner-is-Offline"
            )
        else:
            self.logger.info("the Bobcat's network speed is good")

        return is_network_speed_slow

    def ping(self, backoff_time=FIVE_MINUTES, max_attempts=3):
        """Ping the Bobcat until it connects or attempts are maxed out"""

        if self.dry_run:
            self.logger.debug("Bobcat Autopilot Dry Run 🚧")
            self.logger.warning(
                "Actions such as reboot, reset, resync, and fastsync will be skipped. Wait times will only last 1 second"
            )
            backoff_time = 1

        self.logger.debug(f"Ping the Bobcat ({self.bobcat.ip_address})")

        attempt_count = 0
        while not self.bobcat.ping():

            self.logger.warning("The Bobcat is unreachable")

            self.logger.debug(f"Waiting {int(backoff_time / 60)} Minutes ⏳")
            time.sleep(backoff_time)

            attempt_count += 1
            if attempt_count >= max_attempts:
                raise BobcatConnectionError()

        self.logger.debug("Successfully connected to the Bobcat")

    def _wait_for_loading(self, backoff_time=TEN_MINUTES, max_attempts=6):
        """Wait for the Bobcat when loading"""

        if self.dry_run:
            backoff_time = 1

        self.bobcat.refresh_status()

        attempt_count = 0
        while self.bobcat.status.upper() == "LOADING":

            self.logger.info("The Bobcat is still loading")

            self.logger.debug(f"Waiting {int(backoff_time / 60)} Minutes ⏳")
            time.sleep(backoff_time)

            self.bobcat.refresh_status()  # get new status after waiting

            attempt_count += 1
            if attempt_count >= max_attempts:
                self.logger.warning(
                    f"The Bobcat is still loading despite {max_attempts} checks over the last {int(backoff_time / 60) * max_attempts} minutes"
                )
                self.logger.debug(
                    "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4412906643867-Yellow-Light"
                )
                return  # give up waiting for loading
        else:
            self.logger.debug("The Bobcat has finished loading")

    def wait(self, wait_time=THIRTY_MINUTES, backoff_time=FIVE_MINUTES):
        """Wait for Bobcat connection and loading status"""

        if self.dry_run:
            wait_time = 1

        self.logger.debug(f"Waiting {int(wait_time / 60)} Minutes ⏳")
        time.sleep(wait_time)

        self.ping()

        self._wait_for_loading(backoff_time)

    def reboot(self):
        """Reboot the Bobcat and wait for connection"""

        self.logger.debug("Rebooting the Bobcat")

        if not self.dry_run:
            self.bobcat.reboot()
            self.wait()

        self.logger.debug("Finished rebooting the Bobcat")

    def reset(self, max_attempts=3):
        """Reset the Bobcat and wait for connection or exceeds max attempts"""

        self.logger.debug("Resetting the Bobcat")

        attempt_count = 0
        while self.bobcat.status.upper() in ["ERROR", "DOWN"]:

            if not self.dry_run:
                self.bobcat.reset()
                self.wait()

            attempt_count += 1
            if attempt_count >= max_attempts:
                self.logger.critical(
                    f"The Bobcat is still down despite {max_attempts} reset attempts"
                )
                self.logger.critical("Manual intervention is required")
                self.logger.debug(
                    "Contact Bobcat Support: https://bobcatminer.zendesk.com/hc/en-us/articles/4412998083355-Contact-Support"
                )
                return  # give up on on reset
        else:
            self.logger.debug("Finished resetting the Bobcat")

    def resync(self):
        """Resync the Bobcat and wait for connection"""

        self.logger.debug("Resyncing the Bobcat")

        self.bobcat.refresh_status()

        if not self.dry_run:
            self.bobcat.resync()
            self.wait()

        self.logger.debug("Finished resyncing the Bobcat")

    def fastsync(self):
        """Fastsync the Bobcat until the gap is less than 400 or exceeds max attempts"""

        if self.bobcat.gap < 400:
            self.logger.debug(
                f"Cancelling the fastsync. The blockchain gap ({self.bobcat.gap}) is less than 400."
            )
            return

        if self.bobcat.status.upper() in ["ERROR", "DOWN"] or self.bobcat.error:
            self.logger.warning(f"Cancel fastsync because it only works on a healthly Bobcat")
            return

        self.logger.debug("Fastsyncing the Bobcat")

        max_attempts = 5
        attempt_count = 0

        while self.bobcat.gap > 400:

            if not self.dry_run:
                self.bobcat.fastsync()
                self.wait()

            self.bobcat.refresh_status()

            attempt_count += 1
            if attempt_count >= max_attempts:
                self.logger.error(
                    f"The Bobcat is still not synced despite {max_attempts} fastsync attempts"
                )
                self.logger.debug("Failed to fastsync the Bobcat")
                return  # give up on fastsync
        else:
            self.logger.debug("Finished fastsyncing the Bobcat")

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
        else:
            self.logger.debug("Leave the Bobcat alone because it syncing")

        return not is_gap_growing

    def autosync(self):
        """Automatically sync the Bobcat by monitoring the gap during the proscribed reboot -> fastsync - > reset -> fastsync"""
        self.logger.warning("Attempt to sync the Bobcat")

        if self.is_syncing():
            return True

        self.reboot()
        self.bobcat.refresh_status()

        if self.is_syncing():
            return True

        self.logger.info("The reboot did not fix the Bobcat's syncing issue")
        if self.bobcat.gap > 400:
            self.fastsync()

        if self.is_syncing():
            return True

        self.logger.info("The reboot did not fix the Bobcat's syncing issue")
        self.reset()
        self.fastsync()

        if not self.is_syncing():
            self.logger.critical("The autosync failed")
            self.logger.critical("Manual intervention is required")
            self.logger.debug(
                "Contact Bobcat Support: https://bobcatminer.zendesk.com/hc/en-us/articles/4412998083355-Contact-Support"
            )

        return False

    def run(self):
        """Diagnose and repair bobcat"""

        self.logger.debug("The Bobcat Autopilot is starting")

        try:
            lock = FileLock("/tmp/bobcat-autopilot", timeout=1)

            with lock:

                self.ping()

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
                    self.autosync()

                # Diagnose
                self.diagnose_relay()
                self.diagnose_temp()
                self.diagnose_network_speed()

        except Timeout:
            self.logger.warning("Stopping. Another instance of bobcat-autopilot currently running")

        except BobcatConnectionError:
            self.logger.critical(
                f"The Autopilot was unable to connect to the Bobcat ({self.bobcat.ip_address})"
            )
            self.logger.debug("Please verify the IP address and network connection")
            self.logger.debug(
                "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser"
            )

        except Exception as err:
            self.logger.critical(f"Encountered unexpected error: {str(err)}")

        self.logger.debug("The Bobcat Autopilot is finished 🏁")
