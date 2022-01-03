def unhealthy(bobcat):
    """Repair unhealthy bobcat"""
    if not bobcat.status:
        bobcat.refresh_status()

    if not bobcat.miner:
        bobcat.refresh_miner()

    if bobcat.should_reboot():
        bobcat.reboot()

    bobcat.waiter()

    bobcat.refresh_status()
    bobcat.refresh_miner()

    if bobcat.should_reset():
        bobcat.reset()
        bobcat.refresh_status()

        while bobcat.should_fastsync():
            bobcat.fastsync()
    return None
