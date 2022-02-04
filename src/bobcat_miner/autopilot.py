from filelock import Timeout, FileLock

import os
import requests
import sys

try:
    from diagnoser import *
except:
    from .diagnoser import *
try:
    from constants import *
except:
    from .constants import *
try:
    from errors import *
except:
    from .errors import *


class BobcatAutopilot(Bobcat):
    """A class for the Bobcat Autopilot automation."""

    def __init__(self, *args, **kwargs) -> None:
        try:

            super().__init__(*args, **kwargs)

        except BobcatSearchNetworkError as err:
            self._logger.critical(str(err))
            sys.exit(1)  # 👋

        except (BobcatVerificationError, BobcatNotFoundError) as err:
            msg = "\n".join(
                [
                    f"{err}",
                    "Please verify the IP address and network connection",
                    "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser",
                ]
            )
            self._logger.critical(msg)
            sys.exit(1)  # 👋

        except Exception as err:
            self._logger.exception(f"An unexpected error has occurred: {str(err)}")
            sys.exit(1)  # 👋

    @property
    def checks(self):
        return (
            OnlineStatusCheck(self),
            SyncStatusCheck(self),
            RelayStatusCheck(self),
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

    def run(self):
        """Automatically diagnose and repair the Bobcat!"""
        self._logger.debug("The Bobcat Autopilot is starting 🚀 🚀 🚀")

        try:
            lock = FileLock(self._lock_file, timeout=ONE_DAY)

            with lock:
                self._logger.debug(f"Lock Acquired: {self._lock_file}")

                for check in self.checks:

                    self._logger.debug(f"Checking: {check.name}")

                    if check.check():

                        for step in check.autopilot_repair_steps:
                            func, args, kwargs = (
                                step["func"],
                                step.get("args", []),
                                step.get("kwargs", {}),
                            )
                            func(*args, **kwargs)

                            self.refresh(
                                status=True, miner=True, temp=False, speed=False, dig=False
                            )

                            is_running = self.miner_state.lower() == "running"
                            is_healthy = (
                                not self.autopilot.miner_alert
                                and self.autopilot.status.lower()
                                not in ["loading", "syncing", "synced"]
                            )

                            if is_running and is_healthy:
                                self._logger.info("Repair Status: Complete")

        except Timeout:
            self._logger.warning("Stopping. Another instance of Bobcat Autopilot currently running")
            sys.exit(1)  # 👋

        except BobcatConnectionError as err:
            self._logger.critical(str(err))
            sys.exit(1)  # 👋

        except Exception as err:
            self._logger.exception(f"An unexpected error has occurred: {str(err)}")
            sys.exit(1)  # 👋

        finally:
            # clean up lock file
            if os.path.exists(self._lock_file):
                os.remove(self._lock_file)
                self._logger.debug(f"Lock Released: {self._lock_file}")

            self._logger.debug("The Bobcat Autopilot is finished ✨ 🍰 ✨")
