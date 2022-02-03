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

        except (BobcatVerificationError, BobcatNotFoundError) as err:
            msg = "\n".join(
                [
                    f"{err}",
                    "Please verify the IP address and network connection",
                    "Troubleshooting Guide: https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser",
                ]
            )

            self._logger.critical(msg)

        except Exception as err:
            self._logger.exception(f"An unexpected error has occurred: {str(err)}")

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

        except Exception as err:
            self._logger.exception(f"An unexpected error has occurred: {str(err)}")

        finally:
            self._logger.debug("The Bobcat Autopilot is finished ✨ 🍰 ✨")
