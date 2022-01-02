# bobcat-miner-python

A python SDK for interacting with the bobcat miner.

# Quick Start

```bash
pip install bobcat-miner-python
```

# Usage

```python
import bobcat_miner

bobcat = Bobcat(ip_address="192.168.1.10")

# data refresh
# warning: frequent and repetative refreshes may slow down your bobcat thus negatively effecting rewards.
bobcat.refresh_status()
print(bobcat.status)

bobcat.refresh_miner()
print(bobcat.miner)

bobcat.refresh_speed()
print(bobcat.speed)

bobcat.refresh_dig()
print(bobcat.dig)

bobcat.refresh()

# actions
bobcat.reboot()
bobcat.resync()
bobcat.fastsync()
bobcat.reset()

# diagnostics
bobcat.is_healthy()
bobcat.is_running()
bobcat.is_synced()
bobcat.is_temp_safe()
bobcat.has_errors()
bobcat.is_relayed()
bobcat.should_reboot())
bobcat.should_resync()
bobcat.should_fastsync()
bobcat.should_reset()
```

# Donations

Donations are welcome and appreciated!

![HNT: 14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](./images/wallet.jpg)

HNT: [14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)
