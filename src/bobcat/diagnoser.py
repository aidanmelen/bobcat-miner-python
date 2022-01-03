"""Bobcat Diagnoser: https://www.nowitness.org/troubleshooting"""

import time
import logging


def diagnoser(bobcat):
    """Ensure the Bobcat is healthy"""

    THIRTY_MINUTES = 1800

    logger = logging.getLogger("bobcat")
    logger.setLevel(logging.INFO)

    logger.info("running diagnoser...")

    if not bobcat.can_connect():
        logger.error("Failed to conncet to bobcat ({bobcat.ip_address}). Please check your router for the bobcat's private ip address.")

    if not bobcat.status:
        logger.info("refresh status data")
        bobcat.refresh_status()

    if not bobcat.miner:
        logger.info("refresh miner data")
        bobcat.refresh_miner()

    if bobcat.is_healthy:
        logger.info("bobcat is healthy")
    
    else:

        logger.info("bobcat is unhealthy")

        # Try REBOOT, if not work, try RESET (wait for 30 minutes) -> FAST SYNC  (wait for 30 minutes).

        if bobcat.should_reboot():
            logger.info("bobcat rebooting...")
            bobcat.reboot()

        logger.info("refresh status data")
        bobcat.refresh_status()

        logger.info("refresh miner data")
        bobcat.refresh_miner()

        if bobcat.should_reset():
            logger.info("bobcat is still unhealthy after reboot")
            logger.info("bobcat resetting...")
            bobcat.reset()

            logger.info("waiting for 30 minutes...")
            time.sleep(THIRTY_MINUTES)

            logger.info("refresh status data")
            bobcat.refresh_status()

            while bobcat.should_fastsync():

                logger.info("bobcat fastsync...")
                bobcat.fastsync()

                logger.info("waiting for 30 minutes...")
                time.sleep(THIRTY_MINUTES)

    return None