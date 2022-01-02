
def repair_no_activity(bobcat):
    """My bobcat height doesn't change, syncing, or no activity"""
    if not self.status
        bobcat.refresh_status()
    
    if not self.miner:
        bobcat.refresh_miner()
    
    # TODO check activity
    if not bobcat.is_healthy() or bobcat.has_errors:
        bobcat.reboot()

    # wait

    bobcat.refresh_status()
    bobcat.refresh_miner()

    # TODO check activity
    if bobcat.should_reset():
        bobcat.reset()
        bobcat.refresh_status()

        while bobcat.should_fastsync():
            bobcat.fastsync()
    
    return None

        
