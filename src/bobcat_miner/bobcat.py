from typing import List
from bs4 import BeautifulSoup

import time
import sys

try:
    from api import BobcatAPI
except:
    from .api import BobcatAPI
try:
    from constants import *
except:
    from .constants import *
try:
    from errors import *
except:
    from .errors import *


class Bobcat(BobcatAPI):
    """A class for the Bobcat miner."""

    def __init__(self, *args, **kwargs) -> None:

        try:
            super().__init__(*args, **kwargs)

        except BobcatSearchNetworkError as err:
            self.logger.critical(str(err))
            sys.exit(1)  # 👋

        except (BobcatConnectionError, BobcatVerificationError, BobcatNotFoundError) as err:
            msg = "\n".join(
                [
                    f"{err}",
                    "   Please verify the IP address and network connection",
                    "   Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser",
                ]
            )
            self.logger.critical(msg)
            sys.exit(1)  # 👋

        except Exception as err:
            self.logger.exception(f"An unexpected error has occurred: {str(err)}")
            sys.exit(1)  # 👋

    @property
    def status(self):
        """Get status."""
        if not self._status_data:
            self.refresh_status()
        return self._status_data.get("status")

    @property
    def gap(self):
        """Get gap."""
        if not self._status_data:
            self.refresh_status()
        gap = self._status_data.get("gap")
        return int(gap) if gap.lstrip("-").isdigit() else gap

    @property
    def blockchain_height(self):
        """Get blockchain height."""
        if not self._status_data:
            self.refresh_status()
        blockchain_height = self._status_data.get("blockchain_height")
        return (
            int(blockchain_height) if blockchain_height.lstrip("-").isdigit() else blockchain_height
        )

    @property
    def epoch(self):
        """Get epoch."""
        if not self._status_data:
            self.refresh_status()
        epoch = self._status_data.get("epoch")
        return int(epoch) if epoch.lstrip("-").isdigit() else epoch

    @property
    def tip(self):
        """Get tip. Only available during error state."""
        if not self._status_data:
            self.refresh_status()
        return self._status_data.get("tip")

    @property
    def ota_version(self):
        """Get OTA version."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("ota_version")

    @property
    def region(self):
        """Get region."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("region")

    @property
    def frequency_plan(self):
        """Get frequency plan."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("frequency_plan")

    @property
    def animal(self):
        """Get animal."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("animal")

    @property
    def helium_animal(self):
        """Get animal in Helium format."""
        return " ".join([word.capitalize() for word in self.animal.split("-")])

    @property
    def pubkey(self):
        """Get pubic key."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("pubkey")

    @property
    def miner_state(self):
        """Get miner state."""
        if not self._miner_data:
            self.refresh_miner()
        return str(self._miner_data.get("miner", {}).get("State"))

    @property
    def miner_status(self):
        """Get miner status."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("miner", {}).get("Status")

    @property
    def miner_height(self):
        """Get miner height."""
        if not self._status_data:
            self.refresh_status()
        miner_height = self._status_data.get("miner_height")
        return int(miner_height) if miner_height.lstrip("-").isdigit() else miner_height

    @property
    def miner_alert(self):
        """Get miner status."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("miner_alert", None)

    @property
    def miner_desc(self):
        """Get miner status."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("miner_desc", {})

    @property
    def names(self):
        """Get miner names."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("miner", {}).get("Names")

    @property
    def image(self):
        """Get miner image."""
        # https://bobcatminer.zendesk.com/hc/en-us/articles/4413004080667-Access-Diagnoser-Check-OTA-Version
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("miner", {}).get("Image")

    @property
    def created(self):
        """Get miner created."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("miner", {}).get("Created")

    @property
    def p2p_status(self):
        """Get p2p status."""
        if not self._miner_data:
            self.refresh_miner()
        return "\n".join(self._miner_data.get("p2p_status"))

    @property
    def ports_desc(self):
        """Get port description."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("ports_desc")

    @property
    def ports(self):
        """Get ports."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("ports", {})

    @property
    def private_ip(self):
        """Get private ip."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("private_ip")

    @property
    def public_ip(self):
        """Get public ip."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("public_ip")

    @property
    def peerbook(self):
        """Get peerbook."""
        if not self._miner_data:
            self.refresh_miner()
        return "\n".join(self._miner_data.get("peerbook", []))

    @property
    def timestamp(self):
        """Get timestamp."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("timestamp")

    @property
    def error(self):
        """Get error."""
        if not self._miner_data:
            self.refresh_miner()
        return self._miner_data.get("error", None)

    @property
    def temp0(self):
        """Get CPU temp sensor 0 Celsius."""
        if not self._temp_data:
            self.refresh_temp()
        return int(self._temp_data.get("temp0"))

    @property
    def temp1(self):
        """Get CPU temp sensor 1 in Celsius."""
        if not self._temp_data:
            self.refresh_temp()
        return int(self._temp_data.get("temp1"))

    @property
    def coldest_temp(self):
        """Get the lowest of the CPU temp from the two sensors."""
        return self.temp0 if self.temp0 < self.temp1 else self.temp1

    @property
    def hottest_temp(self):
        """Get the highest of the CPU temp from the two sensors."""
        return self.temp0 if self.temp0 > self.temp1 else self.temp1

    @property
    def temp0_c(self):
        """Get CPU temp sensor 0 in Celsius."""
        return self.temp0

    @property
    def temp1_c(self):
        """Get CPU temp sensor 1 in Celsius."""
        return self.temp1

    @property
    def temp0_f(self):
        """Get CPU temp sensor 0 Fahrenheit."""
        return round(self.temp0 * 1.8 + 32, 1)

    @property
    def temp1_f(self):
        """Get CPU temp sensor 1 in Fahrenheit."""
        return round(self.temp1 * 1.8 + 32, 1)

    @property
    def download_speed(self):
        """Get download speed."""
        if not self._speed_data:
            self.refresh_speed()
        return self._speed_data.get("DownloadSpeed")

    @property
    def upload_speed(self):
        """Get upload speed."""
        if not self._speed_data:
            self.refresh_speed()
        return self._speed_data.get("UploadSpeed")

    @property
    def latency(self):
        """Get latency."""
        if not self._speed_data:
            self.refresh_speed()
        return self._speed_data.get("Latency")

    @property
    def dig_name(self):
        """Get dig name."""
        if not self._dig_data:
            self.refresh_dig()
        return self._dig_data.get("name")

    @property
    def dig_message(self):
        """Get dig message."""
        if not self._dig_data:
            self.refresh_dig()
        return self._dig_data.get("message")

    @property
    def dig_dns(self):
        """Get dig DNS."""
        if not self._dig_data:
            self.refresh_dig()
        return self._dig_data.get("DNS")

    @property
    def dig_records(self):
        """Get dig records."""
        if not self._dig_data:
            self.refresh_dig()
        return self._dig_data.get("records", [])

    @property
    def is_healthy(self):
        """Check the health of the Bobcat."""
        return (
            self.status.lower() in ["loading", "syncing", "synced"]
            and not self.miner_alert
            and not self.error
        )

    def _parse_html(self, html) -> str:
        """Parse HTML and return a str
        Args:
            html (str): The HTML to be parsed.
        Returns:
            (str): The parsed HTML response payload.
        """
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n")

    def reboot(self) -> None:
        """Reboot the Bobcat and wait."""
        if self._dry_run:
            self.logger.warning("Dry Run: Reboot Skipped")
        else:
            self.logger.debug(self._parse_html(self._BobcatAPI__reboot().text))
            self.wait(FIVE_MINUTES)
            self.heartbeat()

    def reset(self) -> None:
        """Reset the Bobcat and wait."""
        if self._dry_run:
            self.logger.warning("Dry Run: Reset Skipped")
        else:
            self.logger.debug(self._parse_html(self._BobcatAPI__reset().text))
            self.wait(FIVE_MINUTES)
            self.heartbeat()

    def resync(self) -> None:
        """Resync the Bobcat and wait."""
        if self._dry_run:
            self.logger.warning("Dry Run: Resync Skipped")
        else:
            self.logger.debug(self._parse_html(self._BobcatAPI__resync().text))
            self.wait(FIVE_MINUTES)
            self.heartbeat()

    def fastsync(self) -> None:
        """Fastsync the Bobcat and wait."""
        if self._dry_run:
            self.logger.warning("Dry Run: Fastsync Skipped")
        else:
            self.refresh_status()

            if not isinstance(self.gap, int):
                self.logger.error(
                    f"Cancelling the Fastsync. Unable to read the blockchain gap ({self.gap})"
                )
                return

            if self.gap <= 400:
                self.logger.warning(
                    f"Cancelling Fastsync because it only works when the gap is larger than 400. The current gap is: {self.gap}"
                )
                return

            if not self.is_healthy:
                self.logger.warning(
                    f"Cancelling Fastsync because it can only be run on a healthy Bobcat. The current status is: {self.status}"
                )
                return

            self.logger.debug(self._parse_html(self._BobcatAPI__fastsync().text))
            self.wait(FIVE_MINUTES)
            self.heartbeat()

    def wait(self, duration) -> None:
        """Wait.

        Args:
            duration (int, optional): An arbitrary duration of time to wait.
        """
        if self._no_wait:
            duration = 1

        self.logger.debug(f"Waiting for {int(duration / 60)} Minutes ⏳")
        time.sleep(duration)

    def wait_for_connection(self, backoff_duration: int, max_attempts: int) -> None:
        """Wait for a Bobcat connection.

        Args:
            backoff_duration int: A backoff duration of time in seconds to wait after connection attempts.
            max_attempts int: The max number of attempts before giving up.
        """
        if self._no_wait:
            backoff_duration = 1

        attempt_count = 0
        while not self.can_connect():
            self.logger.warning(f"The Bobcat ({self.animal}) is unreachable")

            self.wait(backoff_duration)

            attempt_count += 1
            if attempt_count >= max_attempts:
                raise BobcatConnectionError(
                    f"Waited for {int(int(backoff_duration * max_attempts) / 60)} minute{'s' if backoff_duration > 60 else ''} and still cannot connect to {self._hostname}"
                )

    def wait_until_running(self, backoff_duration: int, max_attempts: int) -> None:
        """Wait until the Bobcat is running.

        Args:
            backoff_duration int: A backoff duration of time in seconds to wait after status attempts.
            max_attempts int: The max number of attempts before giving up.
        """
        if self._no_wait:
            backoff_duration = 1

        refresh_kwargs = {
            "status": True,
            "miner": True,
            "temp": False,
            "speed": False,
            "dig": False,
        }
        self.refresh(**refresh_kwargs)

        attempt_count = 0
        while self.miner_state.lower() != "running":

            self.logger.warning(f"The Bobcat ({self.animal}) is not running")

            self.wait(backoff_duration)

            attempt_count += 1
            if attempt_count >= max_attempts:
                self.logger.warning(
                    f"Waited for {int(int(backoff_duration * max_attempts) / 60)} minute{'s' if backoff_duration > 60 else ''} and still not running"
                )
                break

            self.refresh(**refresh_kwargs)

    def heartbeat(self, backoff_duration: int = FIVE_MINUTES, max_attempts: int = 12) -> None:
        """Heartbeat check for a Bobcat. Checks connection and running status. Default total wait time is 1 hour (12 attempts * 5 min).

        Args:
            backoff_duration (int, optional): A backoff duration of time in seconds to wait after connection or status attempts. Defaults to FIVE_MINUTES.
            max_attempts (int, optional): The max number of attempts before giving up. Defaults to 12 attempts.
        """
        self.wait_for_connection(backoff_duration, max_attempts)
        self.wait_until_running(backoff_duration, max_attempts)
        self.logger.info(f"Reconnected to the Bobcat ({self.animal})")
