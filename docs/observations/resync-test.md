# Resync

## Action

### Python

```python
import requests
r = requests.post("http://x.x.x.x/admin/resync", headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"})
r.text
```

### Response Payload

```python
'1: Your miner is going to rest<br>2: Docker is going to be stopped<br>3: Boom! Old blockchain data gone<br>4: Bam! Rebuilding miner data<br>Miner successfully restarted, but it may take 30 minutes to load files from internet, please be patient. 2022-01-20 18:12:28 +0000 UTC<br>'
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

State: Resyncing / Loading snapshot

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Resyncing",
    "gap": "-",
    "miner_height": "-",
    "blockchain_height": "-",
    "epoch": "-",
    "tip": " exit status 1"
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
        "x.x.x.x:44158": "closed/timeout",
        "x.x.x.x:22": "closed/timeout",
        "x.x.x.x:44158": "closed/timeout"
    },
    "private_ip": "x.x.x.x",
    "public_ip": "x.x.x.x",
    "peerbook": null,
    "height": null,
    "temp0": "39 \u00b0C",
    "temp1": "33 \u00b0C",
    "timestamp": "2022-01-20 18:12:19 +0000 UTC",
    "errors": ""
}
```

</details><p></p>

State: Syncing

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Syncing",
    "gap": "1190406",
    "miner_height": "1",
    "blockchain_height": "1190407",
    "epoch": "1"
}
```

```json
{
    "ota_version": "1.0.2.75",
    "region": "us915",
    "frequency_plan": "us915",
    "animal": "fancy-awesome-bobcat",
    "pubkey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "miner": {
        "State": "running",
        "Status": "Up 29 seconds",
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
        "|connected|  no   |",
        "|dialable |  no   |",
        "|nat_type |unknown|",
        "| height  |   1   |",
        "+---------+-------+",
        "",
        ""
    ],
    "miner_height": "1",
    "epoch": "1",
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
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "|                   address                    |     name     |listen_add|connectio| nat  |last_updat|",
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    0     |    2    |unknow| 24.354s  |",
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "",
        "+------------------+--------------------+----------------------------------------+-----------------+",
        "|      local       |       remote       |                  p2p                   |      name       |",
        "+------------------+--------------------+----------------------------------------+-----------------+",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "+------------------+--------------------+----------------------------------------+-----------------+",
        "",
        ""
    ],
    "height": [
        "1    1",
        ""
    ],
    "temp0": "36 \u00b0C",
    "temp1": "33 \u00b0C",
    "timestamp": "2022-01-20 18:12:36 +0000 UTC",
    "errors": ""
}
```

</details><p></p>

State: Error

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Error",
    "gap": "-",
    "miner_height": "-",
    "blockchain_height": "1190408",
    "epoch": "-",
    "tip": " context deadline exceeded"
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
        "Status": "Up 2 minutes",
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
    "temp0": "40 \u00b0C",
    "temp1": "36 \u00b0C",
    "timestamp": "2022-01-20 18:14:42 +0000 UTC",
    "errors": "failed to get peer book. Post \"http://%2Fvar%2Frun%2Fdocker.sock/v1.37/containers/6a2289280243c8558f8ffb83af5cca545f804b3e6518b2044b686f3a4a8ba05c/exec\": context deadline exceeded"
}
```

</details><p></p>

State: Loading

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
        "Status": "Up 3 minutes",
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
    "temp0": "36 \u00b0C",
    "temp1": "36 \u00b0C",
    "timestamp": "2022-01-20 18:15:58 +0000 UTC",
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
    "gap": "3154",
    "miner_height": "1187282",
    "blockchain_height": "1190436",
    "epoch": "31300"
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
        "Status": "Up 20 minutes",
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
        "| height  |1187280|",
        "+---------+-------+",
        "",
        ""
    ],
    "miner_height": "1187280",
    "epoch": "31300",
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
        "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    1     |    4    |non| 262.557s |",
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
        "+------------------+--------------------+----------------------------------------+-----------------+",
        "",
        ""
    ],
    "height": [
        "31300    1187280",
        ""
    ],
    "temp0": "35 \u00b0C",
    "temp1": "32 \u00b0C",
    "timestamp": "2022-01-20 18:32:21 +0000 UTC",
    "errors": ""
}
```

# Time 

this took 20 minutes