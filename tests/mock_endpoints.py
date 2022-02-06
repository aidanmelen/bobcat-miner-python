"""Mock bobcat"""
from unittest.mock import MagicMock
from requests.models import Response

import copy
import json

synced_status_data = {
    "status": "Synced",
    "gap": "0",
    "miner_height": "1148539",
    "blockchain_height": "1148539",
    "epoch": "30157",
}

synced_miner_data = {
    "ota_version": "1.0.2.76",
    "region": "region_us915",
    "frequency_plan": "us915",
    "animal": "fancy-awesome-bobcat",
    "pubkey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "miner": {
        "State": "running",
        "Status": "Up 36 hours",
        "Names": ["/miner"],
        "Image": "quay.io/team-helium/miner:miner-arm64_2021.12.14.0_GA",
        "Created": 1639980913,
    },
    "p2p_status": [
        "+---------+-------+",
        "|  name   |result |",
        "+---------+-------+",
        "|connected|  yes  |",
        "|dialable |  yes  |",
        "|nat_type | none  |",
        "| height  |1148539|",
        "+---------+-------+",
        "",
        "",
    ],
    "miner_height": "1148539",
    "epoch": "30157",
    "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
    "ports": {
        "192.168.0.10:22": "open",
        "192.168.0.10:44158": "open",
        "33.117.96.28:22": "closed/timeout",
        "33.117.96.28:44158": "closed/timeout",
    },
    "private_ip": "192.168.0.10",
    "public_ip": "33.117.96.28",
    "peerbook": [
        "+-----------------------------------------------+--------------+----------+---------+---+----------+",
        "|                    address                    |     name     |listen_add|connectio|nat|last_updat|",
        "+-----------------------------------------------+--------------+----------+---------+---+----------+",
        "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    1     |    7    |non| 293.353s |",
        "+-----------------------------------------------+--------------+----------+---------+---+----------+",
        "",
        "+---------------------------+",
        "|listen_addrs (prioritized) |",
        "+---------------------------+",
        "|/ip4/33.117.96.28/tcp/44158|",
        "+---------------------------+",
        "",
        "+------------------+---------------------+----------------------------------------+----------------+",
        "|      local       |       remote        |                  p2p                   |      name      |",
        "+------------------+---------------------+----------------------------------------+----------------+",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
        "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
        "+------------------+---------------------+----------------------------------------+----------------+",
        "",
        "",
    ],
    "height": ["30157    1148539", ""],
    "temp0": "38 °C",
    "temp1": "37 °C",
    "timestamp": "2021-12-21 18:18:39 +0000 UTC",
    "errors": "",
}

synced_temp_data = {
    "timestamp": "2021-12-21 18:18:39 +0000 UTC",
    "temp0": 38,
    "temp1": 37,
    "unit": "°C",
}

synced_speed_data = {
    "DownloadSpeed": "94 Mbit/s",
    "UploadSpeed": "57 Mbit/s",
    "Latency": "7.669083ms",
}

synced_dig_data = {
    "name": "seed.helium.io.",
    "DNS": "Local DNS",
    "records": [
        {"A": "54.232.171.76", "dial": "success", "ttl": 16},
        {"A": "13.211.2.73", "dial": "success", "ttl": 16},
        {"A": "3.15.87.218", "dial": "success", "ttl": 16},
    ],
}

down_status_data = {
    "status": "Error",
    "gap": "-",
    "miner_height": "-",
    "blockchain_height": "-",
    "epoch": "-",
    "tip": "miner not started. exit status 1",
}
down_miner_data = {
    "ota_version": "1.0.2.75",
    "region": "error: usage in",
    "frequency_plan": "us915",
    "animal": "fancy-awesome-bobcat",
    "pubkey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "miner": {
        "State": "running",
        "Status": "Up 2 seconds",
        "Names": ["/miner"],
        "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.12.1_GA",
        "Created": 1642700322,
    },
    "p2p_status": ["Node 'miner@127.0.0.1' not responding to pings.", ""],
    "miner_height": "{'EXIT',",
    "epoch": "RPC",
    "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
    "ports": {
        "x.x.x.x:22": "open",
        "x.x.x.x:44158": "closed/timeout",
        "x.x.x.x:22": "closed/timeout",
        "x.x.x.x:44158": "closed/timeout",
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
        "",
    ],
    "height": [
        "RPC to 'miner@127.0.0.1' failed: {'EXIT',",
        "                                  {badarg,",
        "                                   [{ets,lookup,",
        '                                     [clique_commands,["info","height"]],',
        "                                     [{error_info,",
        "                                       #{cause => id,",
        "                                         module => erl_stdlib_errors}}]},",
        "                                    {clique_command,match_lookup,1,",
        '                                     [{file,"clique_command.erl"},{line,124}]},',
        "                                    {clique_command,match,1,",
        '                                     [{file,"clique_command.erl"},{line,111}]},',
        "                                    {blockchain_console,command,1,",
        '                                     [{file,"blockchain_console.erl"},',
        "                                      {line,10}]}]}}",
        "",
    ],
    "temp0": "31 \u00b0C",
    "temp1": "30 \u00b0C",
    "timestamp": "2022-01-20 17:38:46 +0000 UTC",
    "errors": "",
}
down_temp_data = {
    "timestamp": "2021-12-21 18:18:39 +0000 UTC",
    "temp0": 78,
    "temp1": 75,
    "unit": "°C",
}
down_speed_data = {
    "DownloadSpeed": "4 Mbit/s",
    "UploadSpeed": "4 Mbit/s",
    "Latency": "110.669083ms",
}
down_dig_data = {
    "name": "",
    "message": "seed.helium.io A records not found",
    "DNS": "Local DNS",
    "records": [],
}


reboot_response_data = "Rebooting hotspot"
reset_response_data = "1: Your miner is going to rest<br>3: Housekeeper was sent home<br>3: Docker is going to be stopped<br>4: Boom! Old blockchain data gone<br>5: Boom! miner gone<br>6: Housekeeper is back, but everything is gone<br>7: Rebuilding everything<br>8: Cleaning up<br>Bam! Miner successfully restarted, but it may take 30 minutes to load files from internet. Please be patient. 2022-01-20 17:39:06 +0000 UTC<br>"
resync_response_data = "1: Your miner is going to rest<br>2: Docker is going to be stopped<br>3: Boom! Old blockchain data gone<br>4: Bam! Rebuilding miner data<br>Miner successfully restarted, but it may take 30 minutes to load files from internet, please be patient. 2022-01-20 18:12:28 +0000 UTC<br>"
fastsync_response_data = "Syncing your miner, please leave your power on."


online_helium_api_response_data = {
    "data": {
        "speculative_nonce": 6,
        "lng": 0.8154535504049,
        "lat": 0.7123168464,
        "timestamp_added": "2021-07-14T16:48:11.000000Z",
        "status": {
            "timestamp": "2022-01-30T03:14:46.738000Z",
            "online": "online",
            "listen_addrs": ["/ip4/33.117.96.28/tcp/44158"],
            "height": 1204332,
        },
        "reward_scale": 0.837982177734375,
        "payer": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "owner": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "nonce": 6,
        "name": "fancy-awesome-bobcat",
        "mode": "full",
        "location_hex": "55555a801fffff",
        "location": "555555a80009bff",
        "last_poc_challenge": 1208016,
        "last_change_block": 1208348,
        "geocode": {
            "short_street": "Main Street",
            "short_state": "UT",
            "short_country": "US",
            "short_city": "Salt Lake City",
            "long_street": "Main Street",
            "long_state": "Utah",
            "long_country": "United States",
            "long_city": "Salt Lake City",
            "city_id": "c2FsdCBsYWtlIGNpdHl1dGFodW5pdGVkIHN0YXRlcw",
        },
        "gain": 58,
        "elevation": 6,
        "block_added": 921761,
        "block": 1208409,
        "address": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    }
}

offline_helium_api_response_data = copy.deepcopy(online_helium_api_response_data)
offline_helium_api_response_data["data"]["status"]["online"] = "offline"


def mock_online(*args, **kwargs):
    response_content = None
    request_url = args[0]

    # bobcat endpoints
    if "/status.json" in request_url:
        response_content = json.dumps(synced_status_data)
    elif "/miner.json" in request_url:
        response_content = json.dumps(synced_miner_data)
    elif "/temp.json" in request_url:
        response_content = json.dumps(synced_temp_data)
    elif "/speed.json" in request_url:
        response_content = json.dumps(synced_speed_data)
    elif "/dig.json" in request_url:
        response_content = json.dumps(synced_dig_data)
    elif "/admin/reboot" in request_url:
        response_content = reboot_response_data
    elif "/admin/reset" in request_url:
        response_content = reset_response_data
    elif "/admin/resync" in request_url:
        response_content = resync_response_data
    elif "/admin/fastsync" in request_url:
        response_content = fastsync_response_data

    # helium endpoints
    elif "api.helium.io/v1/hotspots/" in request_url:
        response_content = json.dumps(online_helium_api_response_data)

    response = Response()
    response.status_code = 200
    response._content = str.encode(response_content)
    return response


def mock_offline(*args, **kwargs):
    response_content = None
    request_url = args[0]

    # bobcat endpoints
    if "/status.json" in request_url:
        response_content = json.dumps(down_status_data)
    elif "/miner.json" in request_url:
        response_content = json.dumps(down_miner_data)
    elif "/temp.json" in request_url:
        response_content = json.dumps(down_temp_data)
    elif "/speed.json" in request_url:
        response_content = json.dumps(down_speed_data)
    elif "/dig.json" in request_url:
        response_content = json.dumps(down_dig_data)
    elif "/admin/reboot" in request_url:
        response_content = reboot_response_data
    elif "/admin/reset" in request_url:
        response_content = reset_response_data
    elif "/admin/resync" in request_url:
        response_content = resync_response_data
    elif "/admin/fastsync" in request_url:
        response_content = fastsync_response_data

    # helium endpoints
    elif "api.helium.io/v1/hotspots" in request_url:
        response_content = json.dumps(offline_helium_api_response_data)

    response = Response()
    response.status_code = 200
    response._content = str.encode(response_content)
    return response
