from filelock import Timeout, FileLock

import os
import requests

try:
    from diagnoser import *
except:
    from .diagnoser import *
try:
    from constants import *
except:
    from .constants import *
try:
    from errors import BobcatConnectionError
except:
    from .errors import BobcatConnectionError


class BobcatAutopilot(Bobcat):
    """A class for the Bobcat Autopilot automation."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @property
    def checks(self):
        return (
            # OnlineStatusCheck(self),
            RelayStatusCheck(self),
            SyncStatusCheck(self),
            NetworkStatusCheck(self),
            TemperatureStatusCheck(self),
            OTAVersionStatusCheck(self),
            DownOrErrorCheck(self),
            HeightAPIErrorCheck(self),
            # NoActivityCheck(self),
            # NoWitnessesCheck(self),
            # BlockChecksumMismatchErrorCheck(self),
            # CompressionMethodorCorruptedErrorCheck(self),
            # TooManyLookupAttemptsErrorCheck(self),
            # OnboardingDewiOrgNxdomainErrorCheck(self),
            # FailedToStartChildErrorCheck(self),
            # NotADetsFileErrorCheck(self),
            # SnapshotsHeliumWTFErrorCheck(self),
            # SnapshotDownloadOrLoadingFailedErrorCheck(self),
            # NoPlausibleBlocksInBatchErrorCheck(self),
            # RPCFailedCheck(self),
        )

    def managed_reboot(self) -> None:
        """Reboot the Bobcat and wait."""
        self._logger.debug(self.reboot())

        if not self._dry_run:
            self.managed_wait()
            self.refresh(status=True, miner=True, temp=False, speed=False, dig=False)

    def managed_reset(self) -> None:
        """Reset the Bobcat and wait."""
        self._logger.debug(self.reset())

        if not self._dry_run:
            self.wait(FIVE_MINUTES)
            self.managed_wait()
            self.refresh(status=True, miner=True, temp=False, speed=False, dig=False)

    def managed_resync(self) -> None:
        """Resync the Bobcat and wait."""
        self._logger.debug(self.refresh_status())

        if not self.gap or isinstance(self.gap, int):
            self._logger.error(
                f"Cancelling the Resync. Unable to read the blockchain gap ({self.gap})"
            )
            return

        self._logger.debug(self.resync())

        if not self._dry_run:
            self.wait(FIVE_MINUTES)
            self.managed_wait()
            self.refresh(status=True, miner=True, temp=False, speed=False, dig=False)

    def managed_fastsync(self) -> None:
        """Fastsync the Bobcat and wait."""
        if not self.gap or isinstance(self.gap, int):
            self._logger.error(
                f"Cancelling the Fastsync. Unable to read the blockchain gap ({self.gap})"
            )
            return

        if self.status.upper() in ["ERROR", "DOWN"] or self.error or self.miner_alert:
            self._logger.warning(
                f"Cancelling Fastsync because it can only be run on a healthy Bobcat. The current status is: {self.status}"
            )
            return

        if self.gap <= 400:
            self._logger.debug(
                f"Cancelling Fastsync because it only works when the gap is larger than 400. The current gap is: {self.gap}"
            )
            return

        self._logger.debug(self.fastsync())

        if not self._dry_run:
            self.managed_wait()
            self.refresh(status=True, miner=True, temp=False, speed=False, dig=False)

    def wait(self, duration) -> None:
        """Wait.

        Args:
            duration (int, optional): An arbitrary duration of time to sleep.
        """
        self._logger.info(f"⏳ Waiting for {int(duration / 60)} Minutes")
        time.sleep(duration)

    def wait_for_connection(self, backoff_duration, max_attempts) -> None:
        """Wait for a Bobcat connection.

        Args:
            backoff_duration (int, optional): A backoff duration of time in seconds to wait after connection attempts.
            max_attempts (int, optional): The max number of attempts before giving up.
        """
        attempt_count = 0
        while not self.can_connect():

            self._logger.warning("The Bobcat ({self.animal}) is unreachable")

            self.wait(backoff_duration)

            attempt_count += 1
            if attempt_count >= max_attempts:
                raise BobcatConnectionError(
                    f"Waited for {int(backoff_duration * max_attempts) / 60} Minute{'s' if duration > 60 else ''} and still cannot connect to {self._hostname}"
                )

    def wait_until_running(self, backoff_duration, max_attempts) -> None:
        """Wait until the Bobcat is running.

        Args:
            backoff_duration (int, optional): A backoff duration of time in seconds to wait after status attempts.
            max_attempts (int, optional): The max number of attempts before giving up.
        """
        attempt_count = 0
        while self.status not in ["Syncing", "Synced"] and not miner_alert:
            self._logger.warning(f"The Bobcat ({self.animal}) is {self.status}")

            self.wait(backoff_duration)

            attempt_count += 1
            if attempt_count >= max_attempts:
                self._logger.warning(
                    f"Waited for {int(backoff_duration * max_attempts) / 60} Minute{'s' if duration > 60 else ''} and still not syncing"
                )

    def managed_wait(self, backoff_duration=FIVE_MINUTES, max_attempts=12) -> None:
        """Wait for a Bobcat connection and running status. Default total wait time is 1 hour (12 attempts * 5 min).

        Args:
            backoff_duration (int, optional): A backoff duration of time in seconds to wait after connection or status attempts. Defaults to FIVE_MINUTES.
            max_attempts (int, optional): The max number of attempts before giving up. Defaults to 12 attempts.
        """
        self.wait_for_connection(backoff_duration, max_attempts)
        self.wait_until_running(backoff_duration, max_attempts)

    def run(self):
        """Automatically diagnose and repair the Bobcat!"""
        self._logger.debug("The Bobcat Autopilot is starting 🚀 🚀 🚀")

        try:
            lock = FileLock(self._lock_file, timeout=ONE_DAY)

            with lock:
                self._logger.debug(f"Lock Acquired: {self._lock_file}")

                # run diagnoser checks
                for check in self.checks:

                    self._logger.debug(f"Checking: {check.name}")

                    if check.check():

                        # run the autopilot repair steps
                        for step in check.autopilot_repair_steps:
                            func, args, kwargs = (
                                step["func"],
                                step.get("args", []),
                                step.get("kwargs", {}),
                            )
                            func(*args, **kwargs)

                            # halt autopilot steps if the bobcat is healthy
                            # is_online = not self.is_offline()
                            # is_synced = not self.is_not_synced()
                            # if is_online and not is_synced:
                            #     self._logger.debug("Bobcat Autopilot Repaired: {check.name}")
                            #     break

            # clean up lock file
            if os.path.exists(self._lock_file):
                os.remove(self._lock_file)
                self._logger.debug(f"Lock Released: {self._lock_file}")

        except Timeout:
            self._logger.warning("Stopping. Another instance of Bobcat Autopilot currently running")

        except (BobcatConnectionError, requests.RequestException) as err:
            self._logger.critical(str(err))
            self._logger.debug("Please verify the IP address and network connection")
            self._logger.debug(
                "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser"
            )

        except Exception as err:
            self._logger.exception(f"An unexpected error has occurred: {str(err)}")

        finally:
            self._logger.debug("The Bobcat Autopilot is finished ✨ 🍰 ✨")
