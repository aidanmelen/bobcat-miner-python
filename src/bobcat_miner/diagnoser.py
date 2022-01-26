from dataclasses import dataclass
from typing import List

import time

try:
    from bobcat import Bobcat
except:
    from .bobcat import Bobcat
try:
    from constants import *
except:
    from .constants import *


@dataclass
class BobcatIssue:
    """Class Bobcat Issues."""

    check: str
    root_cause: str
    description: str
    manual_steps: List[str]
    customer_support_steps: List[str]
    troubleshooting_guide: str


class BobcatDiagnoser:
    """A class for Bobcat Diagnostics."""

    @property
    def issues(self):
        return [
            BobcatIssue(
                check=self.check_down_or_error,
                root_cause="Miner's Docker Container",
                description="This can happen if your miner's Docker crashes. Sometimes losing power or internet connection during an OTA can cause a miner's Docker to crash. This can typically be fixed with a reboot or a reset, followed by a fast sync if your gap is >400. Fast Sync is recommended if your gap is >400 and your miner has been fully synced before.",
                # autopilot_steps=[
                #     {"func": self.managed_reboot},
                #     {"func": self.managed_reset},
                #     {"func": self.managed_fastsync},
                # ],
                manual_steps=[
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
                troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413666097051-Status-Down-4413666097051-Status-Down-",
            ),
            BobcatIssue(
                check=self.check_height_api_error,
                root_cause="Miner's Docker Container",
                description="Sometimes losing power or internet connection during an OTA can cause a miner's Docker to crash resulting in an onboarding error. This crash can manifest itself in the miner not being able to access the correct API.",
                # autopilot_steps=[
                #     {"func": self.managed_reboot},
                #     {"func": self.managed_reset},
                #     {"func": self.managed_fastsync},
                # ],
                manual_steps=[
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
                troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413699665435-API-Error",
            ),
            # BobcatIssue(
            #     check=self.check_no_activity_error,
            #     error_msg="No Proof of Coverage activity",
            #     root_cause="Your miner not being connected to the blockchain. You have not participated in Proof of Coverage activity for some time.",
            #     description="This can happen for a variety of reasons: (1) Your miner could have lost internet connection; or (2) your miner's Docker could have crashed as a result of you losing power or internet connectivity during an OTA.",
            #     autopilot_steps=[
            #         {"func": self.managed_reboot},
            #         # TODO poll activity
            #         {"func": self.managed_reset},
            #         {"func": self.managed_fastsync},
            #     ],
            #     manual_steps=[
            #         "First Try Reboot and wait an hour.",
            #         "If the error persists, unplug the miner then plug it back in. Wait an Hour. If the problem continues proceed to step 3.",
            #         "Reset the miner and wait an hour for the miner to completely start back up.",
            #     ],
            #     customer_support_steps=[
            #         "If possible, send screenshots of your Diagnoser.",
            #         "Tell us what color your LED is.",
            #         "If you can't access your Diagnoser, please open port 22",
            #         "Provide the miner's public IP address.",
            #         "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4414496658715-No-Activity",
            # ),
            # BobcatIssue(
            #     check=self.check_no_witness_error,
            #     error_msg="No Witnesses activity",
            #     root_cause="Your miner not being connected to the blockchain. You have not participated in Proof of Coverage activity for some time.",
            #     description="This can happen for a variety of different reasons. Possible reasons include: Your internet router's firewall settings are blocking LoRa packets before they reach your device. Your ISP has strict firewalls you are not aware of. Call your ISP to confirm. Your antenna is in a non-optimal location. You have the miner deployed in the wrong region. (AU915, US915, EU868, etc). There are too few miner's in your area. You are experiencing a network packet forwarding bug.",
            #     autopilot_steps=[
            #         {"func": self.managed_reset},
            #         {"func": self.managed_fastsync},
            #     ],
            #     manual_steps=[
            #         "First try Reset then Fast Sync" "Then try Resync then Fast Sync",
            #         "Swapping antennas",
            #         "Moving miner/antenna to a different location to test",
            #         "Move the antenna outside to a higher, more visible location",
            #         "Adjust local firewall settings to allow inbound and outbound packets on port 44158",
            #         "OR you can set inbound/outbound pass packet rules at your internet router and confirm those settings with your ISP tech.",
            #         "Double check with your ISP to see if there is a strict firewall.",
            #     ],
            #     customer_support_steps=[
            #         "Confirm you have adjusted your firewall settings. If you have configured pass packet rules in your internet router, please indicate if you have confirmed that these were done correctly.",
            #         "Describe where exactly your antenna is located. Is it inside/outside, on the roof, in a window, on a pole, under a tree, near a building, near a hill? Please be specific.",
            #         "What type of internet service is the miner using, for example: Mobile, Hotspot, Broadband, Cable, DSL Satellite, Fiber Optic…",
            #         "Provide more details about your Network set up, are you on a mesh network, are there additional miners on that network, are you using a VPN, IPV4, IPV6…",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413692547355-No-Witness-",
            # ),
            # BobcatIssue(
            #     check=self.check_block_checksum_mismatch_error,
            #     error_msg="Block Checksum Mismatch",
            #     root_cause="EMMC / Memory issue",
            #     description="This error is related to the EMMC (Embedded MultiMediaCard) in your miner. This is a blockchain error you can potentially snapshot past. This is NOT related to your RAM size.  ",
            #     autopilot_steps=[
            #         {"func": self.managed_reset},
            #         {"func": self.managed_fastsync},
            #     ],
            #     manual_steps=[
            #         "Reset",
            #         "Fast Sync",
            #         "Monitor for Error After it Has Fully Synced",
            #     ],
            #     customer_support_steps=[
            #         "Keep your miner online so that our engineers can work on your miner.",
            #         "You might notice your miner resyncing while our engineers are working on your miner. The process can take some time so please be patient and cooperative.",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
            # ),
            # BobcatIssue(
            #     check=self.check_compression_method_or_corrupted_error,
            #     error_msg="Compression Method or Corrupted",
            #     root_cause="EMMC / Memory issue",
            #     description="This points to an error related to the EMMC (Embedded MultiMediaCard) in your miner. Resyncing might get rid of this error. This is NOT related to your RAM size.",
            #     autopilot_steps=[
            #         {"func": self.managed_resync},
            #         {"func": self.managed_fastsync},
            #     ],
            #     manual_steps=[
            #         "Resync",
            #         "Fastsync",
            #     ],
            #     customer_support_steps=[
            #         "Keep your miner online so that our engineers can work on your issue.",
            #         "You might notice your miner resyncing while our engineers are working on your miner. The process can take some time so please be patient and cooperative.",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
            # ),
            # BobcatIssue(
            #     check=self.check_too_many_lookup_attempts_error,
            #     error_msg="Too Many Lookup Attempts",
            #     root_cause="DNS server settings",
            #     description="This error occurs when your DNS server cannot find the correct nameserver. Normally, the Bobcat miner will automatically add the appropriate nameserver for you.",
            #     autopilot_steps=[],
            #     manual_steps=[
            #         "If this error continues to appear and your miner is not behaving as expected you can try setting your DNS server to 8.8.8.8.",
            #     ],
            #     customer_support_steps=[
            #         "If possible, send screenshots of your Diagnoser.",
            #         "Tell us what color your LED is.",
            #         "If you can't access your Diagnoser, please open port 22",
            #         "Provide the miner's public IP address.",
            #         "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
            # ),
            # BobcatIssue(
            #     check=self.check_oboarding_dewi_org_nxdomain_error,
            #     error_msg="Onboarding Dewi Org Nxdomain",
            #     root_cause="DNS server settings",
            #     description="This error occurs when your DNS server cannot find the correct nameserver. Normally, the Bobcat will automatically add the appropriate nameserver for you.  ",
            #     autopilot_steps=[],
            #     manual_steps=[
            #         "If this error continues to appear and your miner is not behaving as expected you can try setting your DNS server to 8.8.8.8.",
            #     ],
            #     customer_support_steps=[
            #         "If possible, send screenshots of your Diagnoser.",
            #         "Tell us what color your LED is.",
            #         "If you can't access your Diagnoser, please open port 22",
            #         "Provide the miner's public IP address.",
            #         "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
            # ),
            # BobcatIssue(
            #     check=self.check_failed_to_start_child_error,
            #     error_msg="Failed To Start Child",
            #     root_cause="Faulty ECC chip",
            #     description="This usually means that there is either a ECC chip fault or it's a firmware issue. ",
            #     autopilot_steps=[
            #         {"func": self.managed_reset},
            #         {"func": self.managed_fastsync},
            #     ],
            #     manual_steps=[
            #         "Reset",
            #         "Fastsync",
            #     ],
            #     customer_support_steps=[
            #         "If possible, send screenshots of your Diagnoser.",
            #         "Tell us what color your LED is.",
            #         "If you can't access your Diagnoser, please open port 22",
            #         "Provide the miner's public IP address.",
            #         "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
            # ),
            # BobcatIssue(
            #     check=self.check_not_a_dets_file_error,
            #     error_msg="Not A Dets File",
            #     root_cause="Broken Blockchain but this shouldn't be an issue anymore with the latest firmware.",
            #     description="There is probably a corruption in the database",
            #     autopilot_steps=["resync", "fastsync"],
            #     manual_steps=[
            #         "Resync",
            #         "Fastsync",
            #     ],
            #     customer_support_steps=[
            #         "If possible, send screenshots of your Diagnoser.",
            #         "Tell us what color your LED is.",
            #         "If you can't access your Diagnoser, please open port 22",
            #         "Provide the miner's public IP address.",
            #         "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
            # ),
            # BobcatIssue(
            #     check=self.check_snapshots_helium_wtf_error,
            #     error_msg="Snapshots Helium WTF",
            #     root_cause="DNS issue",
            #     description="Miner is unable to connect to DNS servers. New Diagnoser should automatically add Google DNS so it should get rid of this issue.",
            #     autopilot_steps=[],
            #     manual_steps=[
            #         "Add 8.8.8.8 to your DNS server",
            #     ],
            #     customer_support_steps=[
            #         "If possible, send screenshots of your Diagnoser.",
            #         "Tell us what color your LED is.",
            #         "If you can't access your Diagnoser please open port 22",
            #         "Provide the miner's public IP address.",
            #         "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            #         "Double check with your ISP to see if there is a strict firewall.",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
            # ),
            # BobcatIssue(
            #     check=self.check_snapshot_download_or_loading_failed_error,
            #     error_msg="Snapshot Download Or Loading Failed",
            #     root_cause="Miner is unable to download the latest snapshot from the blockchain",
            #     description="There may be too many miners trying to download the snapshot at the same time or your internet connection may be too slow.",
            #     autopilot_steps=[],
            #     manual_steps=[
            #         "Check that your miner is connected via ethernet and that your internet connection is stable, otherwise, the situation should eventually sort itself out.",
            #     ],
            #     customer_support_steps=[
            #         "If possible, send screenshots of your Diagnoser.",
            #         "Tell us what color your LED is.",
            #         "If you can't access your Diagnoser, please open port 22",
            #         "Provide the miner's public IP address.",
            #         "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
            # ),
            # BobcatIssue(
            #     check=self.check_no_plausible_blocks_in_batch_error,
            #     error_msg="No Plausible Blocks In Batch",
            #     root_cause="Helium Network Bug error",
            #     description="This is a Helium network bug that affects miners across all manufacturers. Helium is actively trying to solve the issue.",
            #     autopilot_steps=[
            #         {"func": self.managed_reset},
            #         {"func": self.managed_fastsync},
            #     ],
            #     manual_steps=[
            #         "Helium recommends that you continue to resync and reset until your miner is able to get past the snapshot. Unfortunately, if that doesn't work then you will have to wait for Helium OTA update to fix the issue."
            #     ],
            #     customer_support_steps=[
            #         "If possible, send screenshots of your Diagnoser.",
            #         "Tell us what color your LED is.",
            #         "If you can't access your Diagnoser, please open port 22",
            #         "Provide the miner's public IP address.",
            #         "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
            # ),
            # BobcatIssue(
            #     check=self.check_rpc_to_miner_failed_error,
            #     error_msg="RPC to 'miner@127.0.0.1' failed",
            #     root_cause="Docker container or ECC fault",
            #     description="You might see this during a reset, reboot, or OTA. This is related to the status of the ECC chip. If this error goes away then nothing is wrong. If you continue to see the error you can try the following.",
            #     autopilot_steps=[
            #         {"func": self.managed_reboot},
            #         {"func": self.managed_reset},
            #         {"func": self.managed_fastsync},
            #     ],
            #     manual_steps=[
            #         "First Try Reboot",
            #         "Then Try Reset",
            #         "Then Fastsync",
            #         "Make Sure Your Miner is Connected to the Internet. What color is the miner's LED?",
            #     ],
            #     customer_support_steps=[
            #         "If possible, send screenshots of your Diagnoser.",
            #         "Tell us what color your LED is.",
            #         "If you can't access your Diagnoser, please open port 22",
            #         "Provide the miner's public IP address.",
            #         "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            #     ],
            #     troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
            # ),
            BobcatIssue(
                check=self.check_sync_status,
                root_cause="Internet connection or snapshot not loading.",
                description="If the gap keeps getting larger, it could be the case that the internet connection to the miner is unstable. It is always recommended that you sync into the blockchain for the first time with an ethernet cable. Other reasons why you may be experiencing syncing issues include a network bug or a snapshot not loading. If the gap has not changed in over 24 hours, your miner is likely having an issue with the snapshot.",
                # autopilot_steps=[
                #     {"func": self.sleep, "kwargs": {"duration", ONE_DAY}},
                #     {"func": self.managed_resync},
                #     {"func": self.managed_fastsync},
                # ],
                manual_steps=[
                    "Give the miner more time to sync.",
                    "Connect the miner to an ethernet cable for the first time sync.",
                    "Resync then fast sync from the Diagnoser, allow at least 24 hours after fully syncing. If the problem persists, proceed to step 4.",
                    "Reset then fast sync, allow at least 24 hours after fully syncing before reassessing.",
                ],
                customer_support_steps=[
                    "What type of internet service is the miner using, for example: Mobile, Hotspot, Broadband, Cable, DSL Satellite, Fiber Optic…",
                    "Provide more details about your Network set up; are you on a mesh network, are there additional miners on that network, are you using a VPN, IPV4, IPV6…?",
                ],
                troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4414476039451-Syncing-Issues",
            ),
            BobcatIssue(
                check=self.check_relay_status,
                root_cause="Your Internet Router Settings",
                description="This error is related to the EMMC (Embedded MultiMediaCard) in your miner. This is a blockchain error you can potentially snapshot past. This is NOT related to your RAM size.",
                # autopilot_steps=[],
                manual_steps=[
                    "Set Static IP to the Device.",
                    "Enable UPnP or Open Port 44158 to the Device.",
                ],
                customer_support_steps=[
                    "For quickest results start by contacting your ISP technician.",
                    "If still unresolved after calling ISP tech please provide: ",
                    "What type of internet service is the miner using for example Mobile, Hotspot, Broadband, Cable, DSL Satellite, Fiber Optic, etc. ",
                    "Provide more details about your Network set up, are you on a mesh network, are there additional miners on that network, are you using a VPN…  ",
                    "Provide the following screenshots: ",
                    "Router's port forward settings",
                    "Router's UPnP settings, if available",
                    "Router's Firewall Settings",
                    "Any additional router settings you think might help",
                ],
                troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4413699764763-Confirming-Relay-Status-in-Diagnoser",
            ),
            BobcatIssue(
                check=self.check_network_speed_status,
                root_cause="The internet connection is slow.",
                description="A hard wired internet connection with an ethernet cable will reduce syncing issues and will maximize earning potential. Wifi can be unstable and may cause syncing issues.",
                # autopilot_steps=[],
                manual_steps=[
                    "Connect the Bobcat to the internet with a hard wired ethernet cable."
                ],
                customer_support_steps=[],
                troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4409231342363-Miner-is-Offline",
            ),
            BobcatIssue(
                check=self.check_temperature_status,
                root_cause="Red = Above 70°C | Yellow = Between 65°C and 70°C | White = Below 65°C)",
                description="If the temperature is above 65°C, the Diagnoser will show an 'alert' by changing the color of the temperature label on the menu.",
                # autopilot_steps=[],
                manual_steps=["https://www.nowitness.org/diy-enclosure/"],
                customer_support_steps=[],
                troubleshooting_guide="https://bobcatminer.zendesk.com/hc/en-us/articles/4407605756059-Sync-Status-Temp-Monitoring",
            ),
        ]

    def check_down_or_error(self):
        self.logger.debug("Checking: Status Down/Error")

        if is_down := self.status.upper() == "DOWN" or (
            "ERROR" in self.status.upper() and "ERROR RESPONSE FROM DAEMON" in self.tip.upper()
        ):
            self.logger.error("Bobcat Status: Down")

        return is_down

    def check_height_api_error(self):
        self.logger.debug("Checking: Height API Error")

        if has_error := "HEIGHT API ERROR" in self.status.upper():
            self.logger.error("Bobcat Status: Height API Error")

        return has_error

    # def check_no_activity_error(self):
    #     # NotImplemented
    #     return False

    # def check_no_witness_error(self):
    #     # NotImplemented
    #     return False

    # def check_block_checksum_mismatch_error(self):
    #     # NotImplemented
    #     return False

    # def check_compression_method_or_corrupted_error(self):
    #     # NotImplemented
    #     return False

    # def check_too_many_lookup_attempts_error(self):
    #     # NotImplemented
    #     return False

    # def check_oboarding_dewi_org_nxdomain_error(self):
    #     # NotImplemented
    #     return False

    # def check_failed_to_start_child_error(self):
    #     # NotImplemented
    #     return False

    # def check_not_a_dets_file_error(self):
    #     # NotImplemented
    #     return False

    # def check_snapshots_helium_wtf_error(self):
    #     # NotImplemented
    #     return False

    # def check_snapshot_download_or_loading_failed_error(self):
    #     # NotImplemented
    #     return False

    # def check_no_plausible_blocks_in_batch_error(self):
    #     # NotImplemented
    #     return False

    # def check_rpc_to_miner_failed_error(self):
    #     # NotImplemented
    #     return False

    def check_sync_status(self):
        self.logger.debug("Checking: Sync Status")

        not_synced = self.status.upper() != "SYNCED"
        syncing_and_behind = self.status.upper() == "SYNCING" and self.gap > 300

        msg = f"Sync Status: {self.status.capitalize()} (gap:{self.gap})"

        if sync_status := not_synced or syncing_and_behind:
            self.logger.error(msg)
        else:
            self.logger.info(msg)

        return sync_status

    def check_relay_status(self):
        self.logger.debug("Checking: Relay Status")

        is_pub_ip_over_44158 = f"/ip4/{self.public_ip}/tcp/44158" in self.peerbook

        is_nat_type_none = None
        if isinstance(self.p2p_status, dict):
            is_nat_type_none = self.p2p_status.get("nat_type") != "none"
        else:
            is_nat_type_none = "|nat_type | none  |".upper() in self.p2p_status.upper()

        if is_relayed := not is_pub_ip_over_44158 and not is_nat_type_none:
            self.logger.warning("Relay Status: Relayed")
        else:
            self.logger.info("Relay Status: Not Relayed")

        return is_relayed

    def check_network_speed_status(self):
        self.logger.debug("Checking: Network Status")

        download_speed = int(self.download_speed.strip(" Mbit/s"))
        upload_speed = int(self.upload_speed.strip(" Mbit/s"))
        latency = float(self.latency.strip("ms"))

        if is_download_speed_slow := download_speed < 5:
            self.logger.warning(f"Network Status: Download Slow ({self.download_speed})")

        elif is_upload_speed_slow := upload_speed < 5:
            self.logger.warning(f"Network Status: Upload Slow ({self.upload_speed})")

        elif is_latency_high := latency > 50:
            self.logger.warning(f"Network Status: Latency High ({self.upload_speed})")

        else:
            self.logger.info(f"Network Status: Good 🌐")

        return any([is_download_speed_slow, is_upload_speed_slow, is_latency_high])

    def check_temperature_status(self):
        self.logger.debug("Checking: Temperature Status")

        if is_too_cold := self.coldest_temp < 0:
            self.logger.error(f"Temperature Status: Cold ({self.hottest_temp}°C) ❄️")

        elif is_getting_hot := self.hottest_temp >= 65 and self.hottest_temp < 70:
            self.logger.warning(f"Temperature Status: Warm ({self.hottest_temp}°C) 🔥")

        elif is_too_hot := self.hottest_temp >= 70 or self.hottest_temp >= 70:
            self.logger.error(f"Temperature Status: Hot ({self.hottest_temp}°C) 🌋")

        else:
            self.logger.info(f"Temperature Status: Good ({self.hottest_temp}°C) ☀️")

        return is_too_cold and (is_hot_warning or is_hot_error)
