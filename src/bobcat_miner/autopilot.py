"""Bobcat Autopilot"""

import logging
import json
import time
import math

from filelock import Timeout, FileLock

try:
    from .bobcat import Bobcat
except:
    from bobcat import Bobcat


class Autopilot:

    ONE_MINUTE=60
    THIRTY_MINUTES=1800

    def __init__(self, bobcat):
        assert isinstance(bobcat, Bobcat)
        self.bobcat = bobcat
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    
    def diagnose(self):
        try:
            lock = FileLock("/tmp/bobcat-autopilot", timeout=1)

            with lock:
                if self.bobcat.status.upper() == "ERROR" or self.bobcat.status.lower() == "DOWN":
                    # https://bobcatminer.zendesk.com/hc/en-us/articles/4413666097051-Status-Down-4413666097051-Status-Down-
                    self.the_works()
                    
                if "HEIGHT API ERROR".upper() == status.get("status").upper():
                    # https://bobcatminer.zendesk.com/hc/en-us/articles/4413699665435-API-Error
                    self.the_works()

                if self.bobcat.status.upper() == "SYNCING":
                    
        except Timeout:
            logging.warn("Do nothing. Another instance of bobcat-autopilot currently running.") 


    def the_works(self):
        """First Try Reboot -> Then Try Reset -> Then Try Fastsync"""

        # First Try Reboot
        self.bobcat.reboot()

        while not self.bobcat.ping():
            time.sleep(ONE_MINUTE)

        if self.bobcat.status.upper() != "ERROR" or self.bobcat.status.lower() != "DOWN":
            return None

        # Then Try Reset
        self.bobcat.reset()

        while not self.bobcat.ping():
            time.sleep(ONE_MINUTE)

        if self.bobcat.status.upper() != "ERROR" or self.bobcat.status.lower() != "DOWN":
            return None

        # Then Try Fastsync
        max_fastsync_attempts = 5
        fastsync_attempt_count = 0
        while self.bobcat.gap > 400 and (fastsync_attempt_count < max_fastsync_attempts):
            self.bobcat.fastsync()
            fastsync_attempt_count+=1
            time.sleep(THIRTY_MINUTES)
        else:
            print("failed to sync bobcat with the blockchain after 5 fastsync attempts")

        if self.bobcat.status.upper() != "ERROR" or self.bobcat.status.lower() != "DOWN":
            return None


    def is_syncing_issue(self):
        """Poll the gap and check if it is growing over time."""
        if self.bobcat.gap > 400:
        
            # poll gap to 10 times every 3 minutes
            gap_polls = []
            for i in range(10):
                gap_polls.append(self.bobcat.gap)
                time.sleep(180)
            
            # count occurences of growing gap
            last_gap = math.inf
            gap_growth_count = 0
            for gap in gap_polls:
                if gap > last_gap:
                    last_gap = gap
                    gap_growth_count+=1
            
            return gap_growth_count > 5
        
        else:
            return False
