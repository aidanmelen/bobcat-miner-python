[![PyPI](https://img.shields.io/pypi/v/bobcat_miner.svg)](https://pypi.org/project/bobcat-miner/)
[![Tests](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml)

# bobcat-miner

A python SDK for interacting with the bobcat miner.

## Install

```bash
pip install bobcat-miner
```

## Autopilot Usage

:information_source: Follow these [instructions](https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser) to find the bobcat miner's ip address.

```bash
BOBCAT_IP_ADDRESS="192.168.1.100" bobcat-autopilot
```

## Bobcat Usage

```python
import bobcat_miner

bobcat = bobcat_miner.Bobcat("192.168.1.100")

# refresh
bobcat.refresh_status()
bobcat.refresh_miner()
bobcat.refresh_speed()
bobcat.refresh_temp()
bobcat.refresh_dig()
bobcat.refresh()

# properties
bobcat.status
bobcat.gap
bobcat.miner_height
bobcat.blockchain_height
bobcat.epoch
bobcat.tip
bobcat.ota_version
bobcat.region
bobcat.frequency_plan
bobcat.animal
bobcat.name
bobcat.pubkey
bobcat.state
bobcat.miner_status
bobcat.names
bobcat.image
bobcat.created
bobcat.p2p_status
bobcat.ports_desc
bobcat.ports
bobcat.private_ip
bobcat.public_ip
bobcat.peerbook
bobcat.peerbook_miner
bobcat.peerbook_listen_address
bobcat.peerbook_peers
bobcat.timestamp
bobcat.error
bobcat.temp0
bobcat.temp1
bobcat.temp0_c
bobcat.temp1_c
bobcat.temp0_f
bobcat.temp1_f
bobcat.download_speed
bobcat.upload_speed
bobcat.latency
bobcat.dig_name
bobcat.dig_message
bobcat.dig_dns
bobcat.dig_records

# actions
bobcat.ping()
bobcat.reboot()
bobcat.reset()
bobcat.resync()
bobcat.fastsync()
```

:warning: Both `bobcat.refresh_speed()` or `bobcat.refresh()` take about 30 seconds to complete and you should not call them repeatedly. Doing so will slow down your internet speed, which in turn will slow down your miner.

## Advanced Usage

```python
import bobcat_miner

autopilot = bobcat_miner.Autopilot(bobcat)

# diagnostics
autopilot.diagnose_relay()
autopilot.diagnose_temp()
autopilot.diagnose_network_speed()
autopilot.diagnose_sync()

# actions
autopilot.run()
autopilot.reboot_reset_fastsync()
autopilot.wait()
```

:warning: Both `autopilot.autopilot.is_local_network_slow` take about 30 seconds to complete and you should not call them repeatedly. Doing so will slow down your internet speed, which in turn will slow down your miner.

## Troubleshooting

Please see [No Witness's Troubleshooting Guide](https://www.nowitness.org/troubleshooting/) for more information troubleshooting your bobcat miner.

https://bobcatminer.zendesk.com/hc/en-us/articles/4408443160347-Troubleshooting-your-Bobcat-hotspot

## Donations

Donations are welcome and appreciated! :gift: :tada:

[![HNT: 14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](./images/wallet.jpg)](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)

HNT: [14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)
