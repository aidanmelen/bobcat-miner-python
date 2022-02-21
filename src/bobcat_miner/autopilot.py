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
    def error_checks(self) -> List[BobcatCheck]:
        """Error checks.
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
            SyncStatusCheck(*args),
        )

    @property
    def status_checks(self) -> List[BobcatCheck]:
        """Status checks.
        Returns:
            List(BobcatCheck): Diagnostic checks.
        """
        args = [self.bobcat, self.verbose]

        return (
            RelayStatusCheck(*args),
            NetworkStatusCheck(*args),
            TemperatureStatusCheck(*args),
            OTAVersionStatusCheck(*args, self.state_file),
        )

    def run_autopilot_repair_steps(self, check):
        """Run autopilot repair steps."""
        for step in check.autopilot_repair_steps:

            func, args, kwargs = (
                step["func"],
                step.get("args", []),
                step.get("kwargs", {}),
            )
            func(*args, **kwargs)

            self.bobcat.refresh(status=True, miner=True, temp=False, speed=False, dig=False)

            if isinstance(self.bobcat.gap, int):
                if self.bobcat.is_healthy and self.bobcat.gap < 400:
                    self.bobcat.logger.info("Repair Status: Complete")
                    break

    def run(self) -> None:
        """Automatically diagnose and repair the Bobcat!
        Raises:
            Timeout: If fails to acquire lock within the timeout period
            BobcatConnectionError: If a bobcat connection cannot be established.
            Exception: Catch all.
        """
        self.bobcat.logger.debug("The Bobcat Autopilot is starting 🚀 🚀 🚀")

        lock = FileLock(self.lock_file, timeout=0)

        try:
            lock.acquire()
            self.bobcat.logger.debug(f"Lock Acquired: {self.lock_file}")

            OnlineStatusCheck(self.bobcat, self.verbose).check()

            for check in self.error_checks:
                self.bobcat.logger.debug(f"Checking: {check.name}")

                if check.check():
                    self.run_autopilot_repair_steps(check)

                    # skip remaining error checks since bobcat was repaired
                    break

            for check in self.status_checks:
                self.bobcat.logger.debug(f"Checking: {check.name}")

                if check.check():
                    self.run_autopilot_repair_steps(check)

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
            lock.release()
            self.bobcat.logger.debug(f"Lock Released: {self.lock_file}")

            self.bobcat.logger.debug("The Bobcat Autopilot is finished ✨ 🍰 ✨")
