# Reboot

## Action

### Python

```python
import requests
r = requests.post("http://x.x.x.x/admin/reboot", headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"})
r.text
```

### Response Payload

```python
'Rebooting hotspot'
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

State: "Unkown" (with no errors)

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Unkown",
    "gap": "-",
    "miner_height": "-",
    "blockchain_height": "1190364",
    "epoch": "-"
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
        "Status": "Up About a minute",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642699404
    },
    "p2p_status": [
        "+---------+-------+",
        "|  name   |result |",
        "+---------+-------+",
        "|connected|  yes  |",
        "|dialable |  yes  |",
        "|nat_type | none  |",
        "| height  |1190364|",
        "+---------+-------+",
        "",
        ""
    ],
    "miner_height": "1190364",
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
        "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    1     |    6    |non| 73.941s  |",
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
        "31395    1190364",
        ""
    ],
    "temp0": "30 \u00b0C",
    "temp1": "29 \u00b0C",
    "timestamp": "2022-01-20 17:25:04 +0000 UTC",
    "errors": ""
}
```

</details><p></p>

State: "Unkown" (with errors)

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Unkown",
    "gap": "-",
    "miner_height": "-",
    "blockchain_height": "1190364",
    "epoch": "-"
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
    "p2p_status": null,
    "miner_height": "",
    "epoch": "",
    "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
    "ports": {
        "x.x.x.x:22": "closed/timeout",
        "x.x.x.x:44158": "closed/timeout",
        "x.x.x.x:22": "closed/timeout",
        "x.x.x.x:44158": "closed/timeout"
    },
    "private_ip": "x.x.x.x",
    "public_ip": "x.x.x.x",
    "peerbook": null,
    "height": null,
    "temp0": "33 \u00b0C",
    "temp1": "30 \u00b0C",
    "timestamp": "2022-01-20 17:25:31 +0000 UTC",
    "errors": "    miner error"
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
    "blockchain_height": "-",
    "epoch": "-",
    "tip": "miner not started."
}
```

```json
{
    "ota_version": "1.0.2.75",
    "region": "error: usage in",
    "frequency_plan": "us915",
    "animal": "",
    "pubkey": "",
    "miner": {
        "State": "running",
        "Status": "Up 1 second",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642699580
    },
    "p2p_status": [
        "Node 'miner@127.0.0.1' not responding to pings.",
        ""
    ],
    "miner_height": "command",
    "epoch": "Error:",
    "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
    "ports": {
        "x.x.x.x:22": "open",
        "x.x.x.x:44158": "closed/timeout",
        "x.x.x.x:22": "closed/timeout",
        "x.x.x.x:44158": "closed/timeout"
    },
    "private_ip": "x.x.x.x",
    "public_ip": "x.x.x.x",
    "peerbook": [
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "|                   address                    |     name     |listen_add|connectio| nat  |last_updat|",
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    0     |    0    |unknow|  2.336s  |",
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "",
        "+------------------+--------------------+-----------------------------------------+----------------+",
        "|      local       |       remote       |                   p2p                   |      name      |",
        "+------------------+--------------------+-----------------------------------------+----------------+",
        "|/ip4/x.x.x.x/tcp/4|/ip4/18.141.125.188/|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|custom-mango-mon|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/18.223.200.123/|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|tangy-gunmetal-c|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/162.250.120.9/t|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|dandy-cerulean-t|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/54.214.143.149/|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|sharp-blonde-che|",
        "+------------------+--------------------+-----------------------------------------+----------------+",
        "",
        ""
    ],
    "height": [
        "Error: Usage information not found for the given command",
        "",
        "",
        ""
    ],
    "temp0": "32 \u00b0C",
    "temp1": "29 \u00b0C",
    "timestamp": "2022-01-20 17:26:24 +0000 UTC",
    "errors": ""
}
```

</details><p></p>

State: Synced

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Synced",
    "gap": "0",
    "miner_height": "1190364",
    "blockchain_height": "1190364",
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
        "Status": "Up 27 seconds",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642699580
    },
    "p2p_status": [
        "+---------+-------+",
        "|  name   |result |",
        "+---------+-------+",
        "|connected|  yes  |",
        "|dialable |  no   |",
        "|nat_type |unknown|",
        "| height  |1190364|",
        "+---------+-------+",
        "",
        ""
    ],
    "miner_height": "1190364",
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
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "|                   address                    |     name     |listen_add|connectio| nat  |last_updat|",
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    0     |    4    |unknow|  24.87s  |",
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "",
        "+------------------+--------------------+-----------------------------------------+----------------+",
        "|      local       |       remote       |                   p2p                   |      name      |",
        "+------------------+--------------------+-----------------------------------------+----------------+",
        "|/ip4/x.x.x.x/tcp/4|/ip4/18.141.125.188/|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|custom-mango-mon|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/18.223.200.123/|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|tangy-gunmetal-c|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/162.250.120.9/t|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|dandy-cerulean-t|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/54.214.143.149/|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|sharp-blonde-che|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/120.33.0.58/tcp|/p2p/117xu1eiAENo5XcNLKkAtdi7dTiiw8Mw7WWj|passive-caramel-|",
        "+------------------+--------------------+-----------------------------------------+----------------+",
        "",
        ""
    ],
    "height": [
        "31395    1190364",
        ""
    ],
    "temp0": "36 \u00b0C",
    "temp1": "32 \u00b0C",
    "timestamp": "2022-01-20 17:26:50 +0000 UTC",
    "errors": ""
}
```

# Time 

this took 27 seconds