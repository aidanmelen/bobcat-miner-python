# Unknown Error

```
bobcat --hostname x.x.x.x --trace --animal fancy-awesome-bobcat autopilot
🐛 Connected to Bobcat: x.x.x.x
🐛 Refresh: Miner Data{
    "ota_version": "1.0.2.79",
    "region": "error: usage in",
    "frequency_plan": "us915",
    "animal": "fancy-awesome-bobcat",
    "pubkey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "miner": {
        "State": "running",
        "Status": "Up 7 minutes",
        "Names": [
            "/miner"
        ],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.29.0_GA",
        "Created": 1645293650
    },
    "p2p_status": [
        "Error: Usage information not found for the given command",
        "",
        "",
        ""
    ],
    "miner_height": "command",
    "epoch": "Error:",
    "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
    "ports": {
        "x.x.x.x:22": "open",
        "x.x.x.x:44158": "closed/timeout",
        "y.y.y.y:22": "closed/timeout",
        "y.y.y.y:44158": "closed/timeout"
    },
    "private_ip": "x.x.x.x",
    "public_ip": "y.y.y.y",
    "peerbook": [
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "|                   address                    |     name     |listen_add|connectio| nat  |last_updat|",
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "|/p2p/112YUS4TUQy4boxxxxxxxxssssxSx8FDumTn6vtRY|fancy-awesome-|    0     |    3    |unknow| 751.99s  |",
        "+----------------------------------------------+--------------+----------+---------+------+----------+",
        "",
        "+------------------+--------------------+-----------------------------------------+----------------+",
        "|      local       |       remote       |                   p2p                   |      name      |",
        "+------------------+--------------------+-----------------------------------------+----------------+",
        "|/ip4/x.x.x.x/tc|/ip4/z.z.z.z/t|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|other-awesome-bo|",
        "|/ip4/x.x.x.x/tc|/ip4/z.z.z.z/|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|other-awesome-bo|",
        "|/ip4/x.x.x.x/tc|/ip4/z.z.z.z/t|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|other-awesome-bo|",
        "|/ip4/x.x.x.x/tc|/ip4/z.z.z.z/t|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|other-awesome-bo|",
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
    "temp0": "37 \u00b0C",
    "temp1": "34 \u00b0C",
    "timestamp": "2022-02-20 16:45:53 +0000 UTC",
    "errors": ""
}
🐛 Verified Bobcat Animal: fancy-awesome-bobcat
🐛 The Bobcat Autopilot is starting 🚀 🚀 🚀
🐛 Lock Acquired: /etc/bobcat/autopilot.lock
🐛 Checking: Online Status
⚠️ Online Status: Bobcat is running and the Helium API is stale
🐛 Checking: Sync Status
🐛 Refresh: Status Data
{
    "status": "Unkown",
    "gap": "-",
    "miner_height": "command",
    "blockchain_height": "1234527",
    "epoch": "Error:"
}
❌ Sync Status: Unkown (gap:-)
❌ An unexpected error has occurred: 'SyncStatusCheck' object has no attribute 'autopilot_repair_steps'
Traceback (most recent call last):
  File "/app/src/bobcat_miner/autopilot.py", line 96, in run
    for step in check.autopilot_repair_steps:
AttributeError: 'SyncStatusCheck' object has no attribute 'autopilot_repair_steps'
🐛 Lock Released: /etc/bobcat/autopilot.lock
🐛 The Bobcat Autopilot is finished ✨ 🍰 ✨
```