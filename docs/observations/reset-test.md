# Reset

## Action

### Python

```python
import requests
r = requests.post("http://x.x.x.x/admin/reset", headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"})
r.text
```

### Response Payload

```python
'1: Your miner is going to rest<br>3: Housekeeper was sent home<br>3: Docker is going to be stopped<br>4: Boom! Old blockchain data gone<br>5: Boom! miner gone<br>6: Housekeeper is back, but everything is gone<br>7: Rebuilding everything<br>8: Cleaning up<br>Bam! Miner successfully restarted, but it may take 30 minutes to load files from internet. Please be patient. 2022-01-20 17:39:06 +0000 UTC<br>'
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

</details><p></p>

State: Resyncing

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Resyncing",
    "gap": "-",
    "miner_height": "-",
    "blockchain_height": "-",
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
    "temp0": "28 \u00b0C",
    "temp1": "26 \u00b0C",
    "timestamp": "2022-01-20 17:37:13 +0000 UTC",
    "errors": ""
}
```

</details><p></p>

State: Error (miner not started.)

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
        "x.x.x.x:22": "open",
        "x.x.x.x:44158": "closed/timeout",
        "x.x.x.x:22": "closed/timeout",
        "x.x.x.x:44158": "closed/timeout"
    },
    "private_ip": "x.x.x.x",
    "public_ip": "x.x.x.x",
    "peerbook": null,
    "height": null,
    "temp0": "25 \u00b0C",
    "temp1": "25 \u00b0C",
    "timestamp": "2022-01-20 17:37:28 +0000 UTC",
    "errors": "    miner error"
}
```

</details><p></p>

State: (miner not started) + RF starting

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Error",
    "gap": "-",
    "miner_height": "-",
    "blockchain_height": "-",
    "epoch": "-",
    "tip": "miner not started. exit status 1"
}
```

```json
{
    "ota_version": "1.0.2.75",
    "region": "error: usage in",
    "frequency_plan": "us915",
    "animal": "fancy-awesome-bobcat",
    "pubkey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "miner": {
        "State": "running",
        "Status": "Up 2 seconds",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642700322
    },
    "p2p_status": [
        "Node 'miner@127.0.0.1' not responding to pings.",
        ""
    ],
    "miner_height": "{'EXIT',",
    "epoch": "RPC",
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
        "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    0     |    0    |unknow|  1.26s   |",
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "",
        ""
    ],
    "height": [
        "RPC to 'miner@127.0.0.1' failed: {'EXIT',",
        "                                  {badarg,",
        "                                   [{ets,lookup,",
        "                                     [clique_commands,[\"info\",\"height\"]],",
        "                                     [{error_info,",
        "                                       #{cause => id,",
        "                                         module => erl_stdlib_errors}}]},",
        "                                    {clique_command,match_lookup,1,",
        "                                     [{file,\"clique_command.erl\"},{line,124}]},",
        "                                    {clique_command,match,1,",
        "                                     [{file,\"clique_command.erl\"},{line,111}]},",
        "                                    {blockchain_console,command,1,",
        "                                     [{file,\"blockchain_console.erl\"},",
        "                                      {line,10}]}]}}",
        ""
    ],
    "temp0": "31 \u00b0C",
    "temp1": "30 \u00b0C",
    "timestamp": "2022-01-20 17:38:46 +0000 UTC",
    "errors": ""
}
```

</details><p></p>

State: Syncing (peerbook: null)

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Syncing",
    "gap": "1190374",
    "miner_height": "1",
    "blockchain_height": "1190375",
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
        "Status": "Up 24 seconds",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642700322
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
    "peerbook": null,
    "height": [
        "1    1",
        ""
    ],
    "temp0": "33 \u00b0C",
    "temp1": "30 \u00b0C",
    "timestamp": "2022-01-20 17:39:08 +0000 UTC",
    "errors": ""
}
```

</details><p></p>

State: Syncing (with no errors)

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Syncing",
    "gap": "1190375",
    "miner_height": "1",
    "blockchain_height": "1190376",
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
        "Status": "Up 44 seconds",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642700322
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
        "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    0     |    2    |unknow|  40.07s  |",
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "",
        "+------------------+--------------------+------------------------------------------+---------------+",
        "|      local       |       remote       |                   p2p                    |     name      |",
        "+------------------+--------------------+------------------------------------------+---------------+",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobca|",
        "+------------------+--------------------+------------------------------------------+---------------+",
        "",
        ""
    ],
    "height": [
        "1    1",
        ""
    ],
    "temp0": "33 \u00b0C",
    "temp1": "32 \u00b0C",
    "timestamp": "2022-01-20 17:39:29 +0000 UTC",
    "errors": ""
}
```

</details><p></p>

State: Syncing (with errors)

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Syncing",
    "gap": "1190377",
    "miner_height": "1",
    "blockchain_height": "1190378",
    "epoch": "1"
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
        "Status": "Up About a minute",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642700322
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
    "temp0": "37 \u00b0C",
    "temp1": "34 \u00b0C",
    "timestamp": "2022-01-20 17:40:13 +0000 UTC",
    "errors": "failed to get peer book. Post \"http://%2Fvar%2Frun%2Fdocker.sock/v1.37/containers/4b743c3f2305ff6f5339bd0f80b8ca11778c18a54fd1202b558d1da7c05f2a06/exec\": context deadline exceeded"
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
        "Status": "Up 2 minutes",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642700322
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
    "temp1": "34 \u00b0C",
    "timestamp": "2022-01-20 17:41:30 +0000 UTC",
    "errors": "failed to get peer book. Post \"http://%2Fvar%2Frun%2Fdocker.sock/v1.37/containers/4b743c3f2305ff6f5339bd0f80b8ca11778c18a54fd1202b558d1da7c05f2a06/exec\": context deadline exceeded"
}
```

</details><p></p>

State: Syncing

<details>
  <summary>Click to expand!</summary>

```json
{
    "status": "Syncing",
    "gap": "3118",
    "miner_height": "1187283",
    "blockchain_height": "1190401",
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
        "Status": "Up 21 minutes",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642700322
    },
    "p2p_status": [
        "+---------+---------+",
        "|  name   | result  |",
        "+---------+---------+",
        "|connected|   yes   |",
        "|dialable |   yes   |",
        "|nat_type |symmetric|",
        "| height  | 1187284 |",
        "+---------+---------+",
        "",
        ""
    ],
    "miner_height": "1187284",
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
        "+----------------------------------------------+-------------+---------+---------+-------+---------+",
        "|                   address                    |    name     |listen_ad|connectio|  nat  |last_upda|",
        "+----------------------------------------------+-------------+---------+---------+-------+---------+",
        "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-b|    1    |    7    |symmetr|260.099s |",
        "+----------------------------------------------+-------------+---------+---------+-------+---------+",
        "",
        "+--------------------------------------------------------------------------------------------------+",
        "|                                    listen_addrs (prioritized)                                    |",
        "+--------------------------------------------------------------------------------------------------+",
        "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/p2p-circuit/p2p/xxxxxxxxxxxxxxxxxxxxxxxx|",
        "+--------------------------------------------------------------------------------------------------+",
        "",
        "+-----------------+--------------------+-----------------------------------------+-----------------+",
        "|      local      |       remote       |                   p2p                   |      name       |",
        "+-----------------+--------------------+-----------------------------------------+-----------------+",
        "|/ip4/x.x.x.x/tcp/|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobcat|",
        "|/ip4/x.x.x.x/tcp/|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobcat|",
        "|/ip4/x.x.x.x/tcp/|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobcat|",
        "|/ip4/x.x.x.x/tcp/|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobcat|",
        "|/ip4/x.x.x.x/tcp/|/ip4/x.x.x.x/tcp/441|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobcat|",
        "+-----------------+--------------------+-----------------------------------------+-----------------+",
        "",
        ""
    ],
    "height": [
        "31300    1187284",
        ""
    ],
    "temp0": "43 \u00b0C",
    "temp1": "38 \u00b0C",
    "timestamp": "2022-01-20 18:00:34 +0000 UTC",
    "errors": ""
}
```

# Time 

this took 21 minutes