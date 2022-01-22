from filelock import Timeout, FileLock

import json
import logging
import os
import requests
import time

try:
    from bobcat import Bobcat
except:
    from .bobcat import Bobcat


class BobcatAutopilot(Bobcat):

    DIAGNOSER_STATES = [
        {
            "condition": self.check_down_or_error,
            "diagnosis": "Status Down",
            "root_cause": "Miner's Docker Container",
            "description": "This can happen if your miner's Docker crashes. Sometimes losing power or internet connection during an OTA can cause a miner's Docker to crash. This can typically be fixed with a reboot or a reset, followed by a fast sync if your gap is >400. Fast Sync is recommended if your gap is >400 and your miner has been fully synced before.",
            "repair_steps": [
                self.reboot,
                self.check,
                self.reset,
                self.fastsync,
            ],
            "manual_steps": [
                "First Try Reboot",
                "Try Reset",
                "Then Fastsync",
                "Make Sure Your Miner is Connected to the Internet. What color is your miner's LED?",
            ],
            "customer_support_steps": [
                "If Possible, Screenshots of Your Diagnoser.",
                "Indicate Miner's LED Color",
                "Open Port 22, if Unable to Access the Diagnoser",
                "Provide Miner's IP Address",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413666097051-Status-Down-4413666097051-Status-Down-",
        },
        {
            "condition": self.check_height_api_error,
            "diagnosis": "Height API Error",
            "root_cause": "Miner's Docker Container",
            "description": "Sometimes losing power or internet connection during an OTA can cause a miner's Docker to crash resulting in an onboarding error. This crash can manifest itself in the miner not being able to access the correct API.",
            "autopilot_steps": [
                self.reboot,
                self.check,
                self.reset,
                self.fastsync,
            ],
            "manual_steps": [
                "First Try Reboot",
                "Try Reset",
                "Then Fastsync",
                "Make Sure Your Miner is Connected to the Internet. What color is your miner's LED?",
            ],
            "customer_support_steps": [
                "If Possible, Screenshots of Your Diagnoser.",
                "Indicate Miner's LED Color",
                "Open Port 22, if Unable to Access the Diagnoser",
                "Provide Miner's IP Address",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413699665435-API-Error",
        },
        {
            "condition": self.check_relay,
            "diagnosis": "Relayed",
            "root_cause": "Your Internet Router Settings",
            "description": "This error is related to the EMMC (Embedded MultiMediaCard) in your miner. This is a blockchain error you can potentially snapshot past. This is NOT related to your RAM size.",
            "autopilot_steps": [],
            "manual_steps": [
                "Set Static IP to the Device.",
                "Enable UPnP or Open Port 44158 to the Device.",
            ],
            "customer_support_steps": [
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
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413699764763-Confirming-Relay-Status-in-Diagnoser",
        },
        {
            "condition": self.check_no_activety_error,
            "diagnosis": "No Proof of Coverage activity",
            "root_cause": "Your miner not being connected to the blockchain. You have not participated in Proof of Coverage activity for some time.",
            "description": "This can happen for a variety of reasons: (1) Your miner could have lost internet connection; or (2) your miner's Docker could have crashed as a result of you losing power or internet connectivity during an OTA.",
            "autopilot_steps": [
                self.reboot,
                self.wait,  # hour
            ],
            "manual_steps": [
                "First Try Reboot and wait an hour.",
                "If the error persists, unplug the miner then plug it back in. Wait an Hour. If the problem continues proceed to step 3.",
                "Reset the miner and wait an hour for the miner to completely start back up.",
            ],
            "customer_support_steps": [
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4414496658715-No-Activity",
        },
        {
            "condition": self.check_no_witness_error,
            "diagnosis": "No Witnesses activity",
            "root_cause": "Your miner not being connected to the blockchain. You have not participated in Proof of Coverage activity for some time.",
            "description": "This can happen for a variety of different reasons. Possible reasons include: Your internet router's firewall settings are blocking LoRa packets before they reach your device. Your ISP has strict firewalls you are not aware of. Call your ISP to confirm. Your antenna is in a non-optimal location. You have the miner deployed in the wrong region. (AU915, US915, EU868, etc). There are too few miner's in your area. You are experiencing a network packet forwarding bug.",
            "autopilot_steps": [
                self.reset,
                self.fastsync,
            ],
            "manual_steps": [
                "First try Reset then Fast Sync" "Then try Resync then Fast Sync",
                "Swapping antennas",
                "Moving miner/antenna to a different location to test",
                "Move the antenna outside to a higher, more visible location",
                "Adjust local firewall settings to allow inbound and outbound packets on port 44158",
                "OR you can set inbound/outbound pass packet rules at your internet router and confirm those settings with your ISP tech.",
                "Double check with your ISP to see if there is a strict firewall.",
            ],
            "customer_support_steps": [
                "Confirm you have adjusted your firewall settings. If you have configured pass packet rules in your internet router, please indicate if you have confirmed that these were done correctly.",
                "Describe where exactly your antenna is located. Is it inside/outside, on the roof, in a window, on a pole, under a tree, near a building, near a hill? Please be specific.",
                "What type of internet service is the miner using, for example: Mobile, Hotspot, Broadband, Cable, DSL Satellite, Fiber Optic…",
                "Provide more details about your Network set up, are you on a mesh network, are there additional miners on that network, are you using a VPN, IPV4, IPV6…",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692547355-No-Witness-",
        },
        {
            "condition": self.check_no_witness_error,
            "diagnosis": "Syncing Issue",
            "root_cause": "Internet connection or snapshot not loading.",
            "description": "If the gap keeps getting larger, it could be the case that the internet connection to the miner is unstable. It is always recommended that you sync into the blockchain for the first time with an ethernet cable. Other reasons why you may be experiencing syncing issues include a network bug or a snapshot not loading. If the gap has not changed in over 24 hours, your miner is likely having an issue with the snapshot.",
            "autopilot_steps": [
                self.wait,  # 1 day
                self.resync,
                self.fastsync,
                self.wait,  # 1 day
                self.check,
                self.reset,
                self.fastsync,
            ],
            "manual_steps": [
                "Give the miner more time to sync.",
                "Connect the miner to an ethernet cable for the first time sync.",
                "Resync then fast sync from the Diagnoser, allow at least 24 hours after fully syncing. If the problem persists, proceed to step 4.",
                "Reset then fast sync, allow at least 24 hours after fully syncing before reassessing.",
            ],
            "customer_support_steps": [
                "What type of internet service is the miner using, for example: Mobile, Hotspot, Broadband, Cable, DSL Satellite, Fiber Optic…",
                "Provide more details about your Network set up; are you on a mesh network, are there additional miners on that network, are you using a VPN, IPV4, IPV6…?",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4414476039451-Syncing-Issues",
        },
        {
            "condition": self.check_block_checksum_mismatch_error,
            "diagnosis": "Block Checksum Mismatch",
            "root_cause": "EMMC / Memory issue",
            "description": "This error is related to the EMMC (Embedded MultiMediaCard) in your miner. This is a blockchain error you can potentially snapshot past. This is NOT related to your RAM size.  ",
            "autopilot_steps": [
                self.reset,
                self.fastsync,
            ],
            "manual_steps": [
                "Reset",
                "Fast Sync",
                "Monitor for Error After it Has Fully Synced",
            ],
            "customer_support_steps": [
                "Keep your miner online so that our engineers can work on your miner.",
                "You might notice your miner resyncing while our engineers are working on your miner. The process can take some time so please be patient and cooperative.",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
        },
        {
            "condition": self.check_compression_method_or_corrupted_error,
            "diagnosis": "Compression Method or Corrupted",
            "root_cause": "EMMC / Memory issue",
            "description": "This points to an error related to the EMMC (Embedded MultiMediaCard) in your miner. Resyncing might get rid of this error. This is NOT related to your RAM size.",
            "autopilot_steps": [
                self.sync,
                self.fastsync,
            ],
            "manual_steps": [
                "Resync",
                "Fastsync",
            ],
            "customer_support_steps": [
                "Keep your miner online so that our engineers can work on your issue.",
                "You might notice your miner resyncing while our engineers are working on your miner. The process can take some time so please be patient and cooperative.",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
        },
        {
            "condition": self.check_too_many_lookup_attempts_error,
            "diagnosis": "Too Many Lookup Attempts",
            "root_cause": "DNS server settings",
            "description": "This error occurs when your DNS server cannot find the correct nameserver. Normally, the Bobcat miner will automatically add the appropriate nameserver for you.",
            "manual_steps": [
                "If this error continues to appear and your miner is not behaving as expected you can try setting your DNS server to 8.8.8.8.",
            ],
            "customer_support_steps": [
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
        },
        {
            "condition": self.check_oboarding_dewi_org_nxdomain_error,
            "diagnosis": "Onboarding Dewi Org Nxdomain",
            "root_cause": "DNS server settings",
            "description": "This error occurs when your DNS server cannot find the correct nameserver. Normally, the Bobcat will automatically add the appropriate nameserver for you.  ",
            "manual_steps": [
                "If this error continues to appear and your miner is not behaving as expected you can try setting your DNS server to 8.8.8.8.",
            ],
            "customer_support_steps": [
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
        },
        {
            "condition": self.check_failed_to_start_child_error,
            "diagnosis": "Failed To Start Child",
            "root_cause": "Faulty ECC chip",
            "description": "This usually means that there is either a ECC chip fault or it's a firmware issue. ",
            "autopilot_steps": [
                self.reset,
                self.fastsync,
            ],
            "manual_steps": [
                "Reset",
                "Fastsync",
            ],
            "customer_support_steps": [
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
        },
        {
            "condition": self.check_not_a_dets_file_error,
            "diagnosis": "Not A Dets File",
            "root_cause": "Broken Blockchain but this shouldn't be an issue anymore with the latest firmware.",
            "description": "There is probably a corruption in the database",
            "autopilot_steps": [self.resync, self.fastsync],
            "manual_steps": [
                "Resync",
                "Fastsync",
            ],
            "customer_support_steps": [
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
        },
        {
            "condition": self.check_snapshots_helium_wtf_error,
            "diagnosis": "Snapshots Helium WTF",
            "root_cause": "DNS issue",
            "description": "Miner is unable to connect to DNS servers. New Diagnoser should automatically add Google DNS so it should get rid of this issue.",
            "autopilot_steps": [],
            "manual_steps": [
                "Add 8.8.8.8 to your DNS server",
            ],
            "customer_support_steps": [
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
                "Double check with your ISP to see if there is a strict firewall.",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
        },
        {
            "condition": self.check_snapshot_download_or_loading_failed_error,
            "diagnosis": "Snapshot Download Or Loading Failed",
            "root_cause": "Miner is unable to download the latest snapshot from the blockchain",
            "description": "There may be too many miners trying to download the snapshot at the same time or your internet connection may be too slow.",
            "autopilot_steps": [],
            "manual_steps": [
                "Check that your miner is connected via ethernet and that your internet connection is stable, otherwise, the situation should eventually sort itself out.",
            ],
            "customer_support_steps": [
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
        },
        {
            "condition": self.check_no_plausible_blocks_in_batch_error,
            "diagnosis": "No Plausible Blocks In Batch",
            "root_cause": "Helium Network Bug error",
            "description": "This is a Helium network bug that affects miners across all manufacturers. Helium is actively trying to solve the issue.",
            "autopilot_steps": [
                self.reset,
                self.fastsync,
            ],
            "manual_steps": [
                "Helium recommends that you continue to resync and reset until your miner is able to get past the snapshot. Unfortunately, if that doesn't work then you will have to wait for Helium OTA update to fix the issue."
            ],
            "customer_support_steps": [
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
        },
        {
            "condition": self.check_rpc_to_miner_failed_error,
            "diagnosis": "RPC to 'miner@127.0.0.1' failed",
            "root_cause": "Docker container or ECC fault",
            "description": "You might see this during a reset, reboot, or OTA. This is related to the status of the ECC chip. If this error goes away then nothing is wrong. If you continue to see the error you can try the following.",
            "autopilot_steps": [
                self.wait,
                self.check,
                self.reboot,
                self.check,
                self.reset,
                self.fastsync,
            ],
            "manual_steps": [
                "First Try Reboot",
                "Then Try Reset",
                "Then Fastsync",
                "Make Sure Your Miner is Connected to the Internet. What color is the miner's LED?",
            ],
            "customer_support_steps": [
                "If possible, send screenshots of your Diagnoser.",
                "Tell us what color your LED is.",
                "If you can't access your Diagnoser, please open port 22",
                "Provide the miner's public IP address.",
                "Confirm Port 22 is Open (Include a Screenshot of this Page)",
            ],
            "troubleshooting_guide": "https://bobcatminer.zendesk.com/hc/en-us/articles/4413692565659-Common-Error-Logs-in-Miner-5s-",
        },
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_relayed(self) -> bool:
        """Diagnose the relay."""

        self.logger.debug("Checking Relay Status")
        self.logger.info("Relay Status: Not Relayed")
        self.logger.warning("Relay Status: Relayed")
        self.logger.error("Status: ERROR")
        self.logger.critical("Status: CRITICAL!!!")

    def run(self):
        self.refresh_status()
        print(self.status)


if __name__ == "__main__":
    import os

    ip_address = os.getenv("BOBCAT_IP_ADDRESS")
    discord_webhook_url = os.getenv("BOBCAT_DISCORD_WEBHOOK_URL")

    # autopilot = BobcatAutopilot(ip_address, log_level_stream="INFO", log_level_file="DEBUG", log_file="/var/log/bobcat.log", log_level_discord="WARN", discord_webhook_url=discord_webhook_url)
    autopilot = BobcatAutopilot(
        ip_address, log_file="/var/log/bobcat.log", discord_webhook_url=discord_webhook_url
    )
    autopilot.is_relayed()
