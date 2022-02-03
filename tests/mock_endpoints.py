"""Mock bobcat"""
from requests.models import Response

import json


def mock_synced_bobcat(*args, **kwargs):
    response_content = None
    request_url = args[0]
    if "/status.json" in request_url:
        response_content = json.dumps(
            {
                "status": "Synced",
                "gap": "0",
                "miner_height": "1148539",
                "blockchain_height": "1148539",
                "epoch": "30157",
            }
        )
    elif "/miner.json" in request_url:
        response_content = json.dumps(
            {
                "ota_version": "1.0.2.66",
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
        )
    elif "/temp.json" in request_url:
        response_content = json.dumps(
            {
                "timestamp": "2021-12-21 18:18:39 +0000 UTC",
                "temp0": 38,
                "temp1": 37,
                "unit": "°C",
            }
        )
    elif "/speed.json" in request_url:
        response_content = json.dumps(
            {
                "DownloadSpeed": "94 Mbit/s",
                "UploadSpeed": "57 Mbit/s",
                "Latency": "7.669083ms",
            }
        )
    elif "/dig.json" in request_url:
        response_content = json.dumps(
            {
                "name": "seed.helium.io.",
                "DNS": "Local DNS",
                "records": [
                    {"A": "54.232.171.76", "dial": "success", "ttl": 16},
                    {"A": "13.211.2.73", "dial": "success", "ttl": 16},
                    {"A": "3.15.87.218", "dial": "success", "ttl": 16},
                ],
            }
        )
    response = Response()
    response.status_code = 200
    response._content = str.encode(response_content)
    return response


def mock_helium_api_online(*args, **kwargs):
    response_content = json.dumps(
        {
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
    )
    response = Response()
    response.status_code = 200
    response._content = str.encode(response_content)
    return response


def mock_helium_api_offline(*args, **kwargs):
    response_content = json.dumps(
        {
            "data": {
                "speculative_nonce": 6,
                "lng": 0.8154535504049,
                "lat": 0.7123168464,
                "timestamp_added": "2021-07-14T16:48:11.000000Z",
                "status": {
                    "timestamp": "2022-01-30T03:14:46.738000Z",
                    "online": "offline",
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
    )
    response = Response()
    response.status_code = 200
    response._content = str.encode(response_content)
    return response
