[![PyPI](https://img.shields.io/pypi/v/bobcat_miner.svg)](https://pypi.org/project/bobcat-miner/)

# bobcat-miner

A python SDK for interacting with the bobcat miner.

## Install

```bash
pip install bobcat-miner
```

## Autopilot Usage

Run autopilot against a healthy bobcat

```bash
$ BOBCAT_IP_ADDRESS="x.x.x.x" bobcat-autopilot
2022-01-03 20:26:30,433 INFO starting bobcat autopilot...
2022-01-03 20:26:33,494 INFO refreshing status data...
2022-01-03 20:26:34,999 INFO refreshing miner data...
2022-01-03 20:26:45,749 INFO bobcat is healthy
```

Run autopilot against an unhealthy bobcat

```bash
$ BOBCAT_IP_ADDRESS="x.x.x.x" bobcat-autopilot
2022-01-03 20:26:30,433 INFO starting bobcat autopilot...
2022-01-03 20:26:33,494 INFO refreshing status data...
2022-01-03 20:26:34,999 INFO refreshing miner data...
2022-01-03 20:26:45,749 INFO bobcat is unhealthy
2022-01-03 20:26:47,472 INFO bobcat rebooting...
2022-01-03 20:31:33,594 INFO refreshing status data...
2022-01-03 20:31:53,989 INFO refreshing miner data...
2022-01-03 20:39:23,989 INFO bobcat is still unhealthy after reboot
2022-01-03 20:40:34,712 INFO bobcat resetting...
2022-01-03 21:10:32,182 INFO waiting for 30 minutes...
2022-01-03 21:12:54,941 INFO refreshing status data...
2022-01-03 21:13:47,912 INFO bobcat fastsync...
2022-01-03 21:14:23,673 INFO waiting for 30 minutes...
2022-01-03 21:45:12,492 INFO bobcat is healthy
```

## Bobcat Usage

```python
import bobcat_miner

bobcat = bobcat_miner.Bobcat(ip_address="x.x.x.x")

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

# autopilot
bobcat.autopilot()
```

:warning: `bobcat.refresh_speed()` takes about 30 seconds to complete and you should not call it repeatedly. Doing so will slow down your internet speed, which in turn will slow down your miner.

## Troubleshooting

Please see [No Witness's Troubleshooting Guide](https://www.nowitness.org/troubleshooting/) for more information troubleshooting your bobcat miner.

## Donations

Donations are welcome and appreciated!

[![HNT: 14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](./images/wallet.jpg)](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)

HNT: [14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)
