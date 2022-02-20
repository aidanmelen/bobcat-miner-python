from typing import List
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

    def __init__(
        self,
        bobcat: Bobcat,
        lock_file: str = ".bobcat.lock",
        state_file: str = ".bobcat.json",
        verbose: bool = False,
    ) -> None:
        """The Bobcat Autopilot constructor.

        Args:
            bobcat (Bobcat): The Bobcat instance to autopilot.
            lock_file (str): The lock file path.
            state_file (str): The state file path.
            verbose (bool): Verbose diagnostic debug logging.
        """

        assert isinstance(bobcat, Bobcat)
        self.bobcat = bobcat

        self.lock_file = lock_file
        self.state_file = state_file
        self.verbose = verbose

    @property
    def checks(self) -> List[BobcatCheck]:
        """Diagnostic checks.
        Returns:
            List(BobcatCheck): Diagnostic checks.
        """
        args = [self.bobcat, self.verbose]

        return (
            DownOrErrorCheck(*args),
            HeightAPIErrorCheck(*args),
            # TODO checks not implemented
            # NoActivityCheck(*args),
            # NoWitnessesCheck(*args),
            # BlockChecksumMismatchErrorCheck(*args),
            # CompressionMethodorCorruptedErrorCheck(*args),
            # TooManyLookupAttemptsErrorCheck(*args),
            # OnboardingDewiOrgNxdomainErrorCheck(*args),
            # FailedToStartChildErrorCheck(*args),
            # NotADetsFileErrorCheck(*args),
            # SnapshotsHeliumWTFErrorCheck(*args),
            # SnapshotDownloadOrLoadingFailedErrorCheck(*args),
            # NoPlausibleBlocksInBatchErrorCheck(*args),
            # RPCFailedCheck(*args),
            UnknownErrorCheck(*args),
            OnlineStatusCheck(*args),
            SyncStatusCheck(*args),
            RelayStatusCheck(*args),
            NetworkStatusCheck(*args),
            TemperatureStatusCheck(*args),
            OTAVersionStatusCheck(*args, self.state_file),
        )

    def run(self) -> None:
        """Automatically diagnose and repair the Bobcat!"""
        self.bobcat.logger.debug("The Bobcat Autopilot is starting 🚀 🚀 🚀")

        try:
            lock = FileLock(self.lock_file, timeout=ONE_DAY)

            with lock:
                self.bobcat.logger.debug(f"Lock Acquired: {self.lock_file}")

                for check in self.checks:

                    self.bobcat.logger.debug(f"Checking: {check.name}")

                    if check.check():

                        for step in check.autopilot_repair_steps:
                            func, args, kwargs = (
                                step["func"],
                                step.get("args", []),
                                step.get("kwargs", {}),
                            )
                            func(*args, **kwargs)

                            self.bobcat.refresh(
                                status=True, miner=True, temp=False, speed=False, dig=False
                            )

                            is_running = self.bobcat.miner_state.lower() == "running"
                            if is_running and self.bobcat.is_healthy:
                                self.bobcat.logger.info("Repair Status: Complete")

        except Timeout:
            self.bobcat.logger.warning(
                "Stopping. Another instance of Bobcat Autopilot currently running"
            )
            sys.exit(1)  # 👋

        except BobcatConnectionError as err:
            self.bobcat.logger.critical(str(err))
            sys.exit(1)  # 👋

        except Exception as err:
            self.bobcat.logger.exception(f"An unexpected error has occurred: {str(err)}")
            sys.exit(1)  # 👋

        finally:
            # clean up lock file
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
                self.bobcat.logger.debug(f"Lock Released: {self.lock_file}")

            self.bobcat.logger.debug("The Bobcat Autopilot is finished ✨ 🍰 ✨")
