from dataclasses import dataclass
from filelock import Timeout, FileLock

import json
import os
import requests
import time

try:
    from bobcat import Bobcat
except:
    from .bobcat import Bobcat
try:
    from diagnoser import BobcatDiagnoser
except:
    from .diagnoser import BobcatDiagnoser
try:
    from errors import BobcatConnectionError
except:
    from .errors import BobcatConnectionError
try:
    from constants import *
except:
    from .constants import *


class BobcatAutopilot(Bobcat, BobcatDiagnoser):
    """A class for the Bobcat Autopilot automation."""

    def __init__(self, *args, **kwargs):
        self.lock_file = kwargs.pop("lock_file", ".bobcat.lock")
        super().__init__(*args, **kwargs)

    def managed_reboot(self):
        """Reboot the Bobcat and wait."""
        self.logger.info(self.reboot())
        self.wait()

    def managed_reset(self):
        """Reset the Bobcat and wait."""
        self.logger.info(self.reset())
        self.sleep()
        self.wait()

    def managed_resync(self):
        """Resync the Bobcat and wait."""
        self.refresh_status()

        if not self.gap or isinstance(self.gap, str):
            self.logger.error(
                f"Cancelling the Resync. Unable to read the blockchain gap ({self.gap})"
            )
            return

        self.logger.info(self.resync())
        self.sleep()
        self.wait()

    def managed_fastsync(self):
        """Fastsync the Bobcat and wait."""
        if not self.gap or isinstance(self.gap, str):
            self.logger.error(
                f"Cancelling the Fastsync. Unable to read the blockchain gap ({self.gap})"
            )
            return

        if self.status.upper() in ["ERROR", "DOWN"] or self.error:
            self.logger.warning(
                f"Cancelling Fastsync because it can only be run on a healthy Bobcat. The current status is: {self.status}"
            )
            return

        if self.gap <= 400:
            self.logger.debug(
                f"Cancelling Fastsync because it only works when the gap is larger than 400. The current gap is: {self.gap}"
            )
            return

        self.logger.info(self.fastsync())
        self.wait()

    def sleep(self, duration=FIVE_MINUTES):
        """Sleep.

        Args:
            duration (int, optional): An arbitrary duration of time to sleep. Defaults to FIVE_MINUTES.
        """
        if self.dry_run:
            self.logger.warning(
                f"Dry run is enabled: ⏳ Sleeping for 1 Second instead of {int(duration / 60)} Minute{'s' if duration > 60 else ''}"
            )
            time.sleep(ONE_SECOND)
        else:
            self.logger.info(f"⏳ Sleeping for {int(duration / 60)} Minutes")
            time.sleep(duration)

    def wait_for_connection(self, backoff_duration, max_attempts) -> None:
        """Wait for a Bobcat connection.

        Args:
            backoff_duration (int, optional): A backoff duration of time in seconds to wait after connection attempts.
            max_attempts (int, optional): The max number of attempts before giving up.
        """
        attempt_count = 0
        while not self.can_connect():

            self.logger.warning("The Bobcat ({self.animal}) is unreachable")

            if self.dry_run:
                self.logger.debug(
                    f"Dry run is enabled: ⏳ Waiting for 1 Second instead of {int(duration / 60)} Minute{'s' if duration > 60 else ''}"
                )
                time.sleep(backoff_duration)
            else:
                self.logger.debug(
                    f"⏳ Waiting {int(backoff_duration / 60)} Minute{'s' if backoff_duration > 60 else ''}"
                )
                time.sleep(backoff_duration)

            attempt_count += 1
            if attempt_count >= max_attempts:
                raise BobcatConnectionError(
                    f"Waited for {int(backoff_duration * max_attempts) / 60} Minute{'s' if duration > 60 else ''} and still cannot connect to {self.hostname}"
                )

    def wait_until_running(self, backoff_duration, max_attempts) -> None:
        """Wait until the Bobcat is running.

        Args:
            backoff_duration (int, optional): A backoff duration of time in seconds to wait after status attempts.
            max_attempts (int, optional): The max number of attempts before giving up.
        """
        attempt_count = 0
        while self.status not in ["Syncing", "Synced"] and not miner_alert:
            self.logger.warning(f"The Bobcat ({self.animal}) is {self.status}")

            if self.dry_run:
                self.logger.debug(
                    f"Dry run is enabled: ⏳ Waiting for 1 Second instead of {int(duration / 60)} Minute{'s' if duration > 60 else ''}"
                )
                time.sleep(backoff_duration)
            else:
                self.logger.debug(
                    f"⏳ Waiting {int(backoff_duration / 60)} Minute{'s' if backoff_duration > 60 else ''}"
                )
                time.sleep(backoff_duration)

            attempt_count += 1
            if attempt_count >= max_attempts:
                self.logger.warning(
                    f"Waited for {int(backoff_duration * max_attempts) / 60} Minute{'s' if duration > 60 else ''} and still not syncing"
                )

    def managed_wait(self, backoff_duration=FIVE_MINUTES, max_attempts=12) -> None:
        """Wait for a Bobcat connection and running status. Default total wait time is 1 hour (12 attempts * 5 min).

        Args:
            backoff_duration (int, optional): A backoff duration of time in seconds to wait after connection or status attempts. Defaults to FIVE_MINUTES.
            max_attempts (int, optional): The max number of attempts before giving up. Defaults to 12 attempts.
        """
        wait_for_connection(backoff_duration, max_attempts)
        wait_until_running(backoff_duration, max_attempts)

    def run(self):
        """Automatically diagnose and repair the Bobcat!"""
        self.logger.debug("The Bobcat Autopilot is starting 🚀 🚀 🚀")

        try:
            lock = FileLock(self.lock_file, timeout=ONE_DAY)

            with lock:
                self.logger.debug(f"Lock Acquired: {self.lock_file}")

                # run diagnoser checks
                for issue in self.issues:

                    if issue.check():
                        pass
                        # run the autopilot repair steps
                        # for step in check.autopilot_steps:
                        #     func, args, kwargs = (
                        #         step["func"],
                        #         step.get("args", []),
                        #         step.get("kwargs", {}),
                        #     )
                        #     func(*args, **kwargs)

            # clean up lock file
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
                self.logger.debug(f"Lock Released: {self.lock_file}")

        except Timeout:
            self.logger.warning("Stopping. Another instance of Bobcat Autopilot currently running")

        except (BobcatConnectionError, requests.RequestException) as err:
            self.logger.critical(str(err))
            self.logger.debug("Please verify the IP address and network connection")
            self.logger.debug(
                "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser"
            )

        except Exception as err:
            self.logger.exception(f"An unexpected error has occurred: {str(err)}")

        finally:
            self.logger.debug("The Bobcat Autopilot is finished ✨ 🍰 ✨")
