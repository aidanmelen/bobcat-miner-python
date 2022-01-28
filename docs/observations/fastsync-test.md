# Fastsync

## Action

### Python

```python
import requests
r = requests.post("http://x.x.x.x/admin/fastsync", headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"})
r.text
```

### Response Payload

```python
'Syncing your miner, please leave your power on.'
```

## Result

### Python

<details>
  <summary>Click to expand!</summary>

```python
import backoff
import json
import requests
import time

@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
    max_time=300,
)
def get(url):
    return requests.get(url)

def poll():
    while True:
        print("Polling status.json")
        print(json.dumps(get("http://x.x.x.x/status.json").json(), indent=4))
        time.sleep(5)
        
        print("Polling miner.json")
        print(json.dumps(get("http://x.x.x.x/miner.json").json(), indent=4))
        time.sleep(5)

poll()
```

</details><p></p>

### State Changes

State: Syncing (Resyncing / Loading snapshot)

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Syncing",
    "gap": "3145",
    "miner_height": "1187295",
    "blockchain_height": "1190440",
    "epoch": "31301"
}
```

```json
{
    "ota_version": "1.0.2.75",
    "region": "",
    "frequency_plan": "us915",
    "animal": "fancy-awesome-bobcat",
    "pubkey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "miner": {
        "State": "",
        "Status": "",
        "Names": null,
        "Image": "",
        "Created": 0
    },
    "miner_alert": "alert",
    "miner_desc": "Resyncing / Loading snapshot",
    "p2p_status": null,
    "miner_height": "",
    "epoch": "",
    "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
    "ports": {
        "x.x.x.x:22": "open",
        "x.x.x.x:44158": "open",
        "x.x.x.x:22": "closed/timeout",
        "x.x.x.x:44158": "closed/timeout"
    },
    "private_ip": "x.x.x.x",
    "public_ip": "x.x.x.x",
    "peerbook": null,
    "height": null,
    "temp0": "31 \u00b0C",
    "temp1": "31 \u00b0C",
    "timestamp": "2022-01-20 18:41:30 +0000 UTC",
    "errors": ""
}
```

</details><p></p>

State: Loading (Miner is loading a snapshot, please keep your hotspot online.)

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Loading",
    "gap": "-",
    "miner_height": "-",
    "blockchain_height": "-",
    "epoch": "-",
    "tip": "Miner is loading a snapshot, please keep your hotspot online."
}
```

```json
{
    "ota_version": "1.0.2.75",
    "region": "",
    "frequency_plan": "us915",
    "animal": "fancy-awesome-bobcat",
    "pubkey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "miner": {
        "State": "running",
        "Status": "Up 30 minutes",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642702325
    },
    "miner_alert": "warn",
    "p2p_status": null,
    "miner_height": "",
    "epoch": "",
    "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
    "ports": {
        "x.x.x.x:22": "open",
        "x.x.x.x:44158": "open",
        "x.x.x.x:22": "closed/timeout",
        "x.x.x.x:44158": "closed/timeout"
    },
    "private_ip": "x.x.x.x",
    "public_ip": "x.x.x.x",
    "peerbook": null,
    "height": null,
    "temp0": "38 \u00b0C",
    "temp1": "36 \u00b0C",
    "timestamp": "2022-01-20 18:43:03 +0000 UTC",
    "errors": "failed to get peer book. Post \"http://%2Fvar%2Frun%2Fdocker.sock/v1.37/containers/6a2289280243c8558f8ffb83af5cca545f804b3e6518b2044b686f3a4a8ba05c/exec\": context deadline exceeded"
}
```

</details><p></p>

State: Syncing

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Syncing",
    "gap": "123",
    "miner_height": "1190347",
    "blockchain_height": "1190470",
    "epoch": "31395"
}
```

```json
{
    "ota_version": "1.0.2.75",
    "region": "region_us915",
    "frequency_plan": "us915",
    "animal": "fancy-awesome-bobcat",
    "pubkey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "miner": {
        "State": "running",
        "Status": "Up About an hour",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642702325
    },
    "p2p_status": [
        "+---------+-------+",
        "|  name   |result |",
        "+---------+-------+",
        "|connected|  yes  |",
        "|dialable |  yes  |",
        "|nat_type | none  |",
        "| height  |1190348|",
        "+---------+-------+",
        "",
        ""
    ],
    "miner_height": "1190348",
    "epoch": "31395",
    "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
    "ports": {
        "x.x.x.x:22": "open",
        "x.x.x.x:44158": "open",
        "x.x.x.x:22": "closed/timeout",
        "x.x.x.x:44158": "closed/timeout"
    },
    "private_ip": "x.x.x.x",
    "public_ip": "x.x.x.x",
    "peerbook": [
        "+-----------------------------------------------+--------------+----------+---------+---+----------+",
        "|                    address                    |     name     |listen_add|connectio|nat|last_updat|",
        "+-----------------------------------------------+--------------+----------+---------+---+----------+",
        "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bo|    1     |    6    |non| 100.744s |",
        "+-----------------------------------------------+--------------+----------+---------+---+----------+",
        "",
        "+---------------------------+",
        "|listen_addrs (prioritized) |",
        "+---------------------------+",
        "|/ip4/x.x.x.x/tcp/44158     |",
        "+---------------------------+",
        "",
        "+------------------+--------------------+----------------------------------------+-----------------+",
        "|      local       |       remote       |                  p2p                   |      name       |",
        "+------------------+--------------------+----------------------------------------+-----------------+",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "+------------------+--------------------+----------------------------------------+-----------------+",
        "",
        ""
    ],
    "height": [
        "31395    1190348",
        ""
    ],
    "temp0": "40 \u00b0C",
    "temp1": "37 \u00b0C",
    "timestamp": "2022-01-20 19:05:14 +0000 UTC",
    "errors": ""
}
```

# Time 

this took 30 minutes