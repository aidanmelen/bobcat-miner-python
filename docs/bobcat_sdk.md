# Bobcat SDK

```python
import bobcat_miner

bobcat = bobcat_miner.Bobcat("192.168.1.10")

# refresh
bobcat.refresh_status()
bobcat.refresh_miner()
bobcat.refresh_speed()
bobcat.refresh_temp()
bobcat.refresh_dig()
bobcat.refresh() # all endpoints

# properties
bobcat.status
bobcat.gap
bobcat.blockchain_height
bobcat.epoch
bobcat.tip
bobcat.ota_version
bobcat.region
bobcat.frequency_plan
bobcat.animal
bobcat.helium_animal
bobcat.pubkey
bobcat.state
bobcat.miner_status
bobcat.miner_height
bobcat.miner_alert
bobcat.miner_desc
bobcat.names
bobcat.image
bobcat.created
bobcat.p2p_status
bobcat.ports_desc
bobcat.ports
bobcat.private_ip
bobcat.public_ip
bobcat.peerbook
bobcat.timestamp
bobcat.error
bobcat.temp0
bobcat.temp1
bobcat.coldest_temp
bobcat.hottest_temp
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
bobcat.reboot()
bobcat.reset()
bobcat.resync()
bobcat.fastsync()
```
