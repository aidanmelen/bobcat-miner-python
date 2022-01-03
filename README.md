# bobcat-miner-python

A python SDK for interacting with the bobcat miner.

# Install

```bash
pip install bobcat-miner-python
```

# Bobcat Usage

```python
import bobcat_miner

bobcat = Bobcat(ip_address="192.168.1.10")

# data refresh
bobcat.refresh_status()
print(bobcat.status)
# {"status": "Synced", "gap": "0", "miner_height": "1148539", "blockchain_height": "1148539", "epoch": "30157"}

bobcat.refresh_miner()
print(bobcat.miner)
# {"ota_version": "1.0.2.66", "region": "region_us915", "frequency_plan": "us915", "animal": "my-mocked-miner", ... }

bobcat.refresh_speed()
print(bobcat.speed)
# {"DownloadSpeed": "94 Mbit/s", "UploadSpeed": "57 Mbit/s", "Latency": "7.669083ms"}

bobcat.refresh_dig()
print(bobcat.dig)
# {"name": "seed.helium.io.", "DNS": "Local DNS", "records": [{"A": "54.232.171.76", ... ]}

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

:warning: `bobcat.refresh_speed()` takes about 30 seconds to complete and you should not call it repeatedly. Doing so will slow down your internet speed, which in turn will slow down your miner.

# Autopilot Usage

If the bobcat miner is unhealthy then the autopilot will attempt to repair it.

```python
import os

import bobcat

bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
bobcat.autopilot()
```

# Troubleshooting

Please see [No Witness's Troubleshooting Guide](https://www.nowitness.org/troubleshooting/) for more information troubleshooting your bobcat miner.

# Donations

Donations are welcome and appreciated!

[![HNT: 14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](./images/wallet.jpg)](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)

HNT: [14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)
