from abc import ABC, abstractmethod
from typing import List, Dict

import json
import os
import re
import requests
import time

try:
    from bobcat import Bobcat
except:
    from .bobcat import Bobcat
try:
    from constants import *
except:
    from .constants import *


class BobcatCheck(ABC):
    """An abstract class for a Bobcat Check."""

    def __init__(
        self,
        bobcat: Bobcat,
        verbose: bool,
        name: str,
        root_cause: str,
        description: str,
        autopilot_repair_steps: List[str] = [],
        manual_repair_steps: List[str] = [],
        customer_support_steps: List[str] = [],
        troubleshooting_guides: List[str] = [],
    ):
        """The Bobcat Check constructor.

        Args:
            bobcat (Bobcat): The Bobcat instance to check.
            verbose (bool): Verbose diagnostic debug logging.
            name (str): The name of the check.
            root_cause (str): The root cause of the check.
            description (str): The description of the check.
            autopilot_repair_steps (List[str], optional): The autopilot repairs steps for the check.
            manual_repair_steps (List[str], optional): The manual repairs steps for the check.
            customer_support_steps (List[str], optional): The customer support steps for the check.
            troubleshooting_guides (List[str], optional): The troubleshooting guides for the check.
        """
        assert isinstance(bobcat, Bobcat)
        self.bobcat = bobcat

        self.verbose = verbose
        self.name = name
        self.root_cause = root_cause
        self.description = description
        self.autopilot_repair_steps = autopilot_repair_steps
        self.manual_repair_steps = manual_repair_steps
        self.customer_support_steps = customer_support_steps
        self.troubleshooting_guides = troubleshooting_guides

    @abstractmethod
    def check(self) -> bool:
        """Return True when the check failed."""
        raise NotImplemented

    def __str__(self) -> str:
        manual_repair_steps = "\n".join(
            [f"{idx+1}. {step}" for idx, step in enumerate(self.manual_repair_steps)]
        )
        customer_support_steps = "\n".join(
            [f"{idx+1}. {step}" for idx, step in enumerate(self.customer_support_steps)]
        )
        troubleshooting_guides = "\n".join([f"- {guide}" for guide in self.troubleshooting_guides])

        return f"""
**Points to:** {self.root_cause}

**Why does this happen?** 
{self.description}

**What You Can Try:** 
{manual_repair_steps}

**What to provide customer support if unable to resolve:**
{customer_support_steps}

**Troublesooting Guides:**
{troubleshooting_guides}
"""


class DownOrErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Down or Error Status",
            root_cause="Miner's Docker Container",
            description="This can happen if your miner's Docker crashes. Sometimes losing power or internet connection during an OTA can cause a miner's Docker to crash. This can typically be fixed with a reboot or a reset, followed by a fast sync if your gap is >400. Fast Sync is recommended if your gap is >400 and your miner has been fully synced before.",
            autopilot_repair_steps=[
                {"func": bobcat.reboot},
                {"func": bobcat.reset},
                {"func": bobcat.fastsync},
            ],
            manual_repair_steps=[
                "First Try Reboot",
                "Try Reset",
                "Then Fastsync",
                "Make Sure Your Miner is Connected to the Internet. What color is your miner's LED?",
            ],
            customer_support_steps=[
                "If Possible, Screenshots of Your Diagnoser.",
                "Indicate Miner's LED Color",
                "Open Port 22, if Unable to Access the Diagnoser",
                "Provide Miner's IP Address",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413666097051-Status-Down-4413666097051-Status-Down-"
            ],
        )

    def check(self) -> bool:
        if down_or_error := self.bobcat.status.upper() == "DOWN" or (
            "ERROR" in self.bobcat.status.upper()
            and "ERROR RESPONSE FROM DAEMON" in self.bobcat.tip.upper()
        ):
            self.bobcat.logger.error(
                f"Bobcat Status: {self.bobcat.status.capitalize()}",
                extra={"description": str(self)} if self.verbose else {},
            )

        return down_or_error


class HeightAPIErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Height API Error Status",
            root_cause="Miner's Docker Container",
            description="Sometimes losing power or internet connection during an OTA can cause a miner's Docker to crash resulting in an onboarding error. This crash can manifest itself in the miner not being able to access the correct API.",
            autopilot_repair_steps=[
                {"func": bobcat.reboot},
                {"func": bobcat.reset},
                {"func": bobcat.fastsync},
            ],
            manual_repair_steps=[
                "First Try Reboot",
                "Try Reset",
                "Then Fastsync",
                "Make Sure Your Miner is Connected to the Internet. What color is your miner's LED?",
            ],
            customer_support_steps=[
                "If Possible, Screenshots of Your Diagnoser.",
                "Indicate Miner's LED Color",
                "Open Port 22, if Unable to Access the Diagnoser",
                "Provide Miner's IP Address",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413699665435-API-Error"
            ],
        )

    def check(self) -> bool:
        if has_error := "HEIGHT API ERROR" in self.bobcat.status.upper():
            self.bobcat.logger.error(
                "Bobcat Status: Height API Error",
                extra={"description": str(self)} if self.verbose else {},
            )

        return has_error


class NoActivityCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="No Activity",
            root_cause="Your miner not being connected to the blockchain. You have not participated in Proof of Coverage activity for some time.",
            description="This can happen for a variety of reasons: (1) Your miner could have lost internet connection; or (2) your miner's Docker could have crashed as a result of you losing power or internet connectivity during an OTA.",
            autopilot_repair_steps=[
                {"func": bobcat.reboot},
                # TODO poll activity
                {"func": bobcat.reset},
                {"func": bobcat.fastsync},
            ],
            manual_repair_steps=[
                "First Try Reboot and wait an hour.",
                "If the error persists, unplug the miner then plug it back in. Wait an Hour. If the problem continues proceed to step 3.",
                "Reset the miner and wait an hour for the miner to completely start back up.",
            ],
            customer_support_steps=[
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4414496658715-No-Activity"
            ],
        )

    def check():
        raise NotImplemented


class NoWitnessesCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="No Witnesses",
            root_cause="Your miner not being connected to the blockchain. You have not participated in Proof of Coverage activity for some time.",
            description="This can happen for a variety of different reasons. Possible reasons include: Your internet router's firewall settings are blocking LoRa packets before they reach your device. Your ISP has strict firewalls you are not aware of. Call your ISP to confirm. Your antenna is in a non-optimal location. You have the miner deployed in the wrong region. (AU915, US915, EU868, etc). There are too few miner's in your area. You are experiencing a network packet forwarding bug.",
            autopilot_repair_steps=[
                {"func": bobcat.reset},
                {"func": bobcat.fastsync},
            ],
            manual_repair_steps=[
                "First try Reset then Fast Sync" "Then try Resync then Fast Sync",
                "Swapping antennas",
                "Moving miner/antenna to a different location to test",
                "Move the antenna outside to a higher, more visible location",
                "Adjust local firewall settings to allow inbound and outbound packets on port 44158",
                "OR you can set inbound/outbound pass packet rules at your internet router and confirm those settings with your ISP tech.",
                "Double check with your ISP to see if there is a strict firewall.",
            ],
            customer_support_steps=[
                "Confirm you have adjusted your firewall settings. If you have configured pass packet rules in your internet router, please indicate if you have confirmed that these were done correctly.",
                "Describe where exactly your antenna is located. Is it inside/outside, on the roof, in a window, on a pole, under a tree, near a building, near a hill? Please be specific.",
                "What type of internet service is the miner using, for example: Mobile, Hotspot, Broadband, Cable, DSL Satellite, Fiber Optic...",
                "Provide more details about your Network set up, are you on a mesh network, are there additional miners on that network, are you using a VPN, IPV4, IPV6...",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692547355-No-Witness-"
            ],
        )

    def check():
        raise NotImplemented


class BlockChecksumMismatchErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Block Checksum Mismatch Error",
            root_cause="EMMC / Memory issue",
            description="This error is related to the EMMC (Embedded MultiMediaCard) in your miner. This is a blockchain error you can potentially snapshot past. This is NOT related to your RAM size. ",
            autopilot_repair_steps=[
                {"func": bobcat.reset},
                {"func": bobcat.fastsync},
            ],
            manual_repair_steps=[
                "Reset",
                "Fast Sync",
                "Monitor for Error After it Has Fully Synced",
            ],
            customer_support_steps=[
                "Keep your miner online so that our engineers can work on your miner.",
                "You might notice your miner resyncing while our engineers are working on your miner. The process can take some time so please be patient and cooperative.",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-"
            ],
        )

    def check():
        raise NotImplemented


class CompressionMethodorCorruptedErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Compression Method or Corrupted Error",
            root_cause="EMMC / Memory issue",
            description="This points to an error related to the EMMC (Embedded MultiMediaCard) in your miner. Resyncing might get rid of this error. This is NOT related to your RAM size.",
            autopilot_repair_steps=[
                {"func": bobcat.resync},
                {"func": bobcat.fastsync},
            ],
            manual_repair_steps=[
                "Resync",
                "Fastsync",
            ],
            customer_support_steps=[
                "Keep your miner online so that our engineers can work on your issue.",
                "You might notice your miner resyncing while our engineers are working on your miner. The process can take some time so please be patient and cooperative.",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-"
            ],
        )

    def check():
        raise NotImplemented


class TooManyLookupAttemptsErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Too Many Lookup Attempts Error",
            root_cause="DNS server settings",
            description="This error occurs when your DNS server cannot find the correct nameserver. Normally, the Bobcat miner will automatically add the appropriate nameserver for you.",
            autopilot_repair_steps=[],
            manual_repair_steps=[
                "If this error continues to appear and your miner is not behaving as expected you can try setting your DNS server to 8.8.8.8.",
            ],
            customer_support_steps=[
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-"
            ],
        )

    def check():
        raise NotImplemented


class OnboardingDewiOrgNxdomainErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Onboarding Dewi Org Nxdomain Error",
            root_cause="DNS server settings",
            description="This error occurs when your DNS server cannot find the correct nameserver. Normally, the Bobcat will automatically add the appropriate nameserver for you. ",
            autopilot_repair_steps=[],
            manual_repair_steps=[
                "If this error continues to appear and your miner is not behaving as expected you can try setting your DNS server to 8.8.8.8.",
            ],
            customer_support_steps=[
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-"
            ],
        )

    def check():
        raise NotImplemented


class FailedToStartChildErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Failed To Start Child Error",
            root_cause="Faulty ECC chip",
            description="This usually means that there is either a ECC chip fault or it's a firmware issue.",
            autopilot_repair_steps=[
                {"func": bobcat.reset},
                {"func": bobcat.fastsync},
            ],
            manual_repair_steps=[
                "Reset",
                "Fastsync",
            ],
            customer_support_steps=[
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-"
            ],
        )

    def check():
        raise NotImplemented


class NotADetsFileErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Not A Dets File Error",
            root_cause="Broken Blockchain but this shouldn't be an issue anymore with the latest firmware.",
            description="There is probably a corruption in the database",
            autopilot_repair_steps=["resync", "fastsync"],
            manual_repair_steps=[
                "Resync",
                "Fastsync",
            ],
            customer_support_steps=[
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-"
            ],
        )

    def check():
        raise NotImplemented


class SnapshotsHeliumWTFErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Snapshots Helium WTF Error",
            root_cause="DNS issue",
            description="Miner is unable to connect to DNS servers. New Diagnoser should automatically add Google DNS so it should get rid of this issue.",
            autopilot_repair_steps=[],
            manual_repair_steps=[
                "Add 8.8.8.8 to your DNS server",
            ],
            customer_support_steps=[
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
                "Double check with your ISP to see if there is a strict firewall.",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-"
            ],
        )

    def check():
        raise NotImplemented


class SnapshotDownloadOrLoadingFailedErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Snapshot Download or Loading Failed Error",
            root_cause="Miner is unable to download the latest snapshot from the blockchain",
            description="There may be too many miners trying to download the snapshot at the same time or your internet connection may be too slow.",
            autopilot_repair_steps=[],
            manual_repair_steps=[
                "Check that your miner is connected via ethernet and that your internet connection is stable, otherwise, the situation should eventually sort itself out.",
            ],
            customer_support_steps=[
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-"
            ],
        )

    def check():
        raise NotImplemented


class NoPlausibleBlocksInBatchErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="No Plausible Blocks In Batch Error",
            root_cause="Helium Network Bug error",
            description="This is a Helium network bug that affects miners across all manufacturers. Helium is actively trying to solve the issue.",
            autopilot_repair_steps=[
                {"func": bobcat.reset},
                {"func": bobcat.fastsync},
            ],
            manual_repair_steps=[
                "Helium recommends that you continue to resync and reset until your miner is able to get past the snapshot. Unfortunately, if that doesn't work then you will have to wait for Helium OTA update to fix the issue."
            ],
            customer_support_steps=[
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-"
            ],
        )

    def check():
        raise NotImplemented


class RPCFailedCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="RPC to 'miner@127.0.0.1' failed Error",
            root_cause="Docker container or ECC fault",
            description="You might see this during a reset, reboot, or OTA. This is related to the status of the ECC chip. If this error goes away then nothing is wrong. If you continue to see the error you can try the following.",
            autopilot_repair_steps=[
                {"func": bobcat.reboot},
                {"func": bobcat.reset},
                {"func": bobcat.fastsync},
            ],
            manual_repair_steps=[
                "First Try Reboot",
                "Then Try Reset",
                "Then Fastsync",
                "Make Sure Your Miner is Connected to the Internet. What color is the miner's LED?",
            ],
            customer_support_steps=[
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-"
            ],
        )

    def check():
        raise NotImplemented


class UnknownErrorCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Unknown Error Status",
            root_cause="Miner's Docker Container",
            description="This can happen if your miner's Docker crashes. Sometimes losing power or internet connection during an OTA can cause a miner's Docker to crash. This can typically be fixed with a reboot or a reset, followed by a fast sync if your gap is >400. Fast Sync is recommended if your gap is >400 and your miner has been fully synced before.",
            autopilot_repair_steps=[
                {"func": bobcat.reboot},
                {"func": bobcat.reset},
                {"func": bobcat.fastsync},
            ],
            manual_repair_steps=[
                "First Try Reboot",
                "Try Reset",
                "Then Fastsync",
                "Make Sure Your Miner is Connected to the Internet. What color is your miner's LED?",
            ],
            customer_support_steps=[
                "If Possible, Screenshots of Your Diagnoser.",
                "Indicate Miner's LED Color",
                "Open Port 22, if Unable to Access the Diagnoser",
                "Provide Miner's IP Address",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413666097051-Status-Down-4413666097051-Status-Down-"
            ],
        )

    def check(self) -> bool:
        is_unhealthy = not self.bobcat.is_healthy

        if is_unhealthy:
            self.bobcat.logger.error(
                f"Bobcat Status: {self.bobcat.status.capitalize()}",
                extra={"description": str(self)} if self.verbose else {},
            )

        return is_unhealthy


class OnlineStatusCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Online Status",
            root_cause="The Helium Network sees your Bobcat as Offline.",
            description="This shows the hotspot information that is currently available in the Helium blockchain. Note that this might differ from the actual status of your hotpsot as it takes time for information to propagate from your hotspot to the blockchain.",
            autopilot_repair_steps=[],
            manual_repair_steps=[
                "Check the Diagnoser to see if the Bobcat is running and is healthy.",
                "Give the Helium Network more time to propagate from your hotspot to the blockchain. Wait 24 hours and check again.",
            ],
            customer_support_steps=[
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=["https://www.nowitness.org/troubleshooting/"],
        )

    def _is_offline(self) -> (Dict, None):
        """Get Hotspot data from Helium API."""
        data = requests.get(f"https://api.helium.io/v1/hotspots/{self.bobcat.pubkey}").json()

        if self.bobcat._trace:
            self.bobcat.logger.debug(
                "Refresh: Helium API Data",
                extra={"description": f"\n```\n{json.dumps(data, indent=4)}\n```"},
            )

        return data.get("data", {}).get("status", {}).get("online", "offline").lower() != "online"

    def check(self) -> bool:
        try:
            is_offline = self._is_offline()
        except Exception as err:
            self.bobcat.logger.warning(
                "The Helium API is not responding. Skipping Online Status Check",
                extra={"description": str(self)} if self.verbose else {},
            )
            return False

        else:
            if is_offline:

                is_running = self.bobcat.miner_state.lower() == "running"

                if is_running and self.bobcat.is_healthy:

                    self.bobcat.logger.warning(
                        f"{self.name}: Bobcat is healthy. Helium API needs time to update.",
                        extra={"description": str(self)} if self.verbose else {},
                    )
                    return False

                else:
                    self.bobcat.logger.error(
                        f"{self.name}: Offline",
                        extra={"description": str(self)} if self.verbose else {},
                    )
                    return True
            else:
                self.bobcat.logger.info(f"{self.name}: Online ⭐")
                return False


class SyncStatusCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Sync Status",
            root_cause="Internet connection or snapshot not loading.",
            description="If the gap keeps getting larger, it could be the case that the internet connection to the miner is unstable. It is always recommended that you sync into the blockchain for the first time with an ethernet cable. Other reasons why you may be experiencing syncing issues include a network bug or a snapshot not loading. If the gap has not changed in over 24 hours, your miner is likely having an issue with the snapshot.",
            autopilot_repair_steps=[
                {"func": bobcat.wait, "args": [ONE_DAY]},
                {"func": bobcat.resync},
                {"func": bobcat.fastsync},
                {"func": bobcat.wait, "args": [ONE_DAY]},
            ],
            manual_repair_steps=[
                "Give the miner more time to sync.",
                "Connect the miner to an ethernet cable for the first time sync.",
                "Resync then fast sync from the Diagnoser, allow at least 24 hours after fully syncing. If the problem persists, proceed to step 4.",
                "Reset then fast sync, allow at least 24 hours after fully syncing before reassessing.",
            ],
            customer_support_steps=[
                "What type of internet service is the miner using, for example: Mobile, Hotspot, Broadband, Cable, DSL Satellite, Fiber Optic...",
                "Provide more details about your Network set up; are you on a mesh network, are there additional miners on that network, are you using a VPN, IPV4, IPV6...?",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4414476039451-Syncing-Issues"
            ],
        )

    def check(self) -> bool:
        is_synced = self.bobcat.status.upper() == "SYNCED"
        syncing_and_caught_up = self.bobcat.status.upper() == "SYNCING" and self.bobcat.gap <= 300

        msg = f"{self.name}: {self.bobcat.status.capitalize()} (gap:{self.bobcat.gap})"

        if is_not_synced := not is_synced and not syncing_and_caught_up:
            self.bobcat.logger.error(msg, extra={"description": str(self)} if self.verbose else {})
        else:
            self.bobcat.logger.info(msg + " 💫")

        return is_not_synced


class RelayStatusCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Relay Status",
            root_cause="Your Internet Router Settings",
            description="The Relay status is determined by lib_p2p. Hotspot's connection is being relayed through another Hotspot on the network which may affect mining. If port 44158 is closed, opening the port should solve the relay. A Relayed hotspot may show 'NAT Type Symmetric' or  'NAT Type Restricted' in your Bobcat Diagnoser. Non Relayed hotspot shows 'NAT Type None'. If it's showing 'NAT Type Unknown', that means you need to wait until the NAT Type is found by the miner. To confirm if your hotspot is relayed, you can click the 'Helium Api' menu in your Diagnoser and see if the address is p2p, your hotspot is relayed.",
            autopilot_repair_steps=[],
            manual_repair_steps=[
                "Set Static IP to the Device.",
                "Enable UPnP or Open Port 44158 to the Device.",
            ],
            customer_support_steps=[
                "For quickest results start by contacting your ISP technician.",
                "If still unresolved after calling ISP tech please provide:",
                "What type of internet service is the miner using for example Mobile, Hotspot, Broadband, Cable, DSL Satellite, Fiber Optic, etc.",
                "Provide more details about your Network set up, are you on a mesh network, are there additional miners on that network, are you using a VPN...",
                "Provide the following screenshots:",
                "Router's port forward settings",
                "Router's UPnP settings, if available",
                "Router's Firewall Settings",
                "Any additional router settings you think might help",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4413699764763-Confirming-Relay-Status-in-Diagnoser",
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4409239473691-Relayed-Miner",
            ],
        )

    def check(self) -> bool:
        if not self.bobcat.is_healthy:
            # do not evaluate relay status if the bobcat is unhealthy
            return False

        is_pub_ip_over_44158 = re.search(
            f"(/ip4/)({self.bobcat.public_ip})(/tcp/44158)",
            self.bobcat.peerbook,
            re.IGNORECASE,
        )
        is_nat_type_none = re.search(
            r"\|.*(nat_type).*\|.*(none).*\|", self.bobcat.p2p_status, re.IGNORECASE
        )

        if is_relayed := not is_pub_ip_over_44158 and not is_nat_type_none:
            self.bobcat.logger.warning(
                f"{self.name}: Relayed",
                extra={"description": str(self)} if self.verbose else {},
            )
        else:
            self.bobcat.logger.info(f"{self.name}: Not Relayed ✨")

        return is_relayed


class NetworkStatusCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Network Status",
            root_cause="The internet connection is slow.",
            description="A hard wired internet connection with an ethernet cable will reduce syncing issues and will maximize earning potential. Wifi can be unstable and may cause syncing issues.",
            autopilot_repair_steps=[],
            manual_repair_steps=[
                "Connect the Bobcat to the internet with a hard wired ethernet cable."
            ],
            customer_support_steps=[
                "For quickest results start by contacting your ISP technician.",
                "If still unresolved after calling ISP tech please provide:",
                "What type of internet service is the miner using for example Mobile, Hotspot, Broadband, Cable, DSL Satellite, Fiber Optic, etc.",
                "Provide more details about your Network set up, are you on a mesh network, are there additional miners on that network, are you using a VPN...",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4409231342363-Miner-is-Offline"
            ],
        )

    def check(self) -> bool:
        download_speed = int(self.bobcat.download_speed.strip(" Mbit/s"))
        upload_speed = int(self.bobcat.upload_speed.strip(" Mbit/s"))
        latency = float(self.bobcat.latency.strip("ms"))

        extra = {"description": str(self)} if self.verbose else {}

        if is_download_speed_slow := download_speed <= 5:
            self.bobcat.logger.warning(
                f"Network Status: Download Slow ({self.bobcat.download_speed})", extra=extra
            )

        if is_upload_speed_slow := upload_speed <= 5:
            self.bobcat.logger.warning(
                f"Network Status: Upload Slow ({self.bobcat.upload_speed})", extra=extra
            )

        if is_latency_high := latency > 100.0:
            self.bobcat.logger.warning(
                f"Network Status: Latency High ({self.bobcat.latency})", extra=extra
            )

        is_network_speed_slow = any([is_download_speed_slow, is_upload_speed_slow, is_latency_high])

        if not is_network_speed_slow:
            self.bobcat.logger.info(f"Network Status: Good 📶")

        return is_network_speed_slow


class TemperatureStatusCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="Temperature Status",
            root_cause="Red = Above 70°C | Yellow = Between 65°C and 70°C | White = Below 65°C)",
            description="If the temperature is above 65°C, the Diagnoser will show an 'alert' by changing the color of the temperature label on the menu.",
            autopilot_repair_steps=[],
            manual_repair_steps=["https://www.nowitness.org/diy-enclosure/"],
            customer_support_steps=["None"],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4407605756059-Sync-Status-Temp-Monitoring"
            ],
        )

    def check(self) -> bool:

        extra = {"description": str(self)} if self.verbose else {}

        if is_too_cold := self.bobcat.coldest_temp < 0:
            self.bobcat.logger.error(
                f"Temperature Status: Cold ({self.bobcat.coldest_temp}°C) ❄️", extra=extra
            )

        if is_getting_hot := self.bobcat.hottest_temp >= 65 and self.bobcat.hottest_temp < 70:
            self.bobcat.logger.warning(
                f"Temperature Status: Warm ({self.bobcat.hottest_temp}°C) 🔥", extra=extra
            )

        if is_too_hot := self.bobcat.hottest_temp >= 70 or self.bobcat.hottest_temp >= 70:
            self.bobcat.logger.error(
                f"Temperature Status: Hot ({self.bobcat.hottest_temp}°C) 🌋", extra=extra
            )

        is_temperature_dangerous = is_too_cold or (is_getting_hot or is_too_hot)

        if not is_temperature_dangerous:
            self.bobcat.logger.info(f"Temperature Status: Good ({self.bobcat.hottest_temp}°C) ☀️")

        return is_temperature_dangerous


class OTAVersionStatusCheck(BobcatCheck):
    def __init__(self, bobcat: Bobcat, verbose: str, state_file: str):
        super().__init__(
            bobcat=bobcat,
            verbose=verbose,
            name="OTA Version Change",
            root_cause="The Bobcat OTA Updates may cause the Helium hotspot firmware to crash.",
            description="The Bobcat OTA (Over the Air) Updates are periodic installations of new firmware on your Bobcat Miner that help optimize your miner's functions.",
            autopilot_repair_steps=[],
            manual_repair_steps=[],
            customer_support_steps=[
                "If Possible, Screenshots of Your Diagnoser.",
                "Indicate Miner's LED Color",
                "Open Port 22, if Unable to Access the Diagnoser",
                "Provide Miner's IP Address",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            troubleshooting_guides=[
                "https://bobcatminer.zendesk.com/hc/en-us/articles/4410155816987-Changes-to-My-Miner-During-an-OTA"
            ],
        )

        self.state_file = state_file

        if not os.path.exists(os.path.abspath(os.path.dirname(self.state_file))):
            os.makedirs(os.path.dirname(self.state_file))

        if not os.path.isfile(self.state_file):
            with open(self.state_file, "w") as f:
                json.dump({"ota_version": self.bobcat.ota_version}, f)

    def check(self) -> bool:
        try:
            with open(self.state_file, "r") as f:
                state = json.load(f)
                previous_ota_version = state.get("ota_version", self.bobcat.ota_version)

        except json.decoder.JSONDecodeError as err:
            previous_ota_version = state.get("ota_version", self.bobcat.ota_version)
            with open(self.state_file, "w") as f:
                json.dump({"ota_version": previous_ota_version}, f)

        if did_ota_version_change := previous_ota_version != self.bobcat.ota_version:
            state["ota_version"] = self.bobcat.ota_version
            self.bobcat.logger.warning(
                f"New OTA Version: {self.bobcat.ota_version}",
                extra={"description": str(self)} if self.verbose else {},
            )

        with open(self.state_file, "w") as f:
            json.dump(state, f)

        return did_ota_version_change
