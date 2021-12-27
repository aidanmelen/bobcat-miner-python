"""Unittests for bobcat.py"""
from unittest.mock import patch, call

import unittest

from bobcat import Bobcat


class TestBobcat(unittest.TestCase):
    def setUp(self):
        self.mock_ip_address = "127.0.0.1"
        self.mock_username = "bobcat"
        self.mock_password = "miner"

        self.mock_happy_path_status = {
            "status": "Synced",
            "gap": "0",
            "miner_height": "1148539",
            "blockchain_height": "1148539",
            "epoch": "30157",
        }

        self.mock_sad_path_status = {
            "status": "Not Synced",
            "gap": "15000",
            "miner_height": "1133539",
            "blockchain_height": "1148539",
            "epoch": "30157",
        }

        self.mock_happy_path_miner = {
            "ota_version": "1.0.2.66",
            "region": "region_us915",
            "frequency_plan": "us915",
            "animal": "my-mocked-miner",
            "pubkey": "112YUf4TUQy4bxXRvGjrj6z7XyiSx8FDudTn6vtRYPgoGPnjBGWW",
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
                "192.168.0.8:22": "open",
                "192.168.0.8:44158": "open",
                "33.117.96.28:22": "closed/timeout",
                "33.117.96.28:44158": "closed/timeout",
            },
            "private_ip": "192.168.0.8",
            "public_ip": "33.117.96.28",
            "peerbook": [
                "+-----------------------------------------------+--------------+----------+---------+---+----------+",
                "|                    address                    |     name     |listen_add|connectio|nat|last_updat|",
                "+-----------------------------------------------+--------------+----------+---------+---+----------+",
                "|/p2p/332YUS4TUQy4boXRvGjrj6z7XyiSx8FDxmTn6vtRYP|my-mock-miner |    1     |    7    |non| 293.353s |",
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
                "|/ip4/172.17.0.2/tc|/ip4/33.223.200.123/t|/p2p/2228k7YK3Ufah5qaAp37qe2jw3LaG6ycQUA|mock-peer-1     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.150.110.17/tc|/p2p/332qFc4yctCWyZyFaDhs4ve2ZsNEn1CKS1G|mock-peer-2     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.12.228.218/tc|/p2p/338eczMRVEBBeoCxiYjaZssdcHQXVk9Zokq|mock-peer-3     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.0.245.53/tcp/|/p2p/33Uyz1JBMcatg4SVYRRk2cxTz3tzvaKcFR7|mock-peer-4     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.37.13.24/tcp/|/p2p/33afuQSrmka2mgxLu91AdtDXbJ9wmqWBUxC|mock-peer-5     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.197.157.248/t|/p2p/33i6EevWXa6cskJepj8UnwMaKkPabZgK6QN|mock-peer-6     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.230.47.214/tc|/p2p/33sogMFP3m6Vgh2hsb3YCaRmG4GpyHdA1HH|mock-peer-7     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.68.166.175/tc|/p2p/33vTBsa1iXjy7QmFs6HFTSqK8ckSejQ3nwZ|mock-peer-8     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.238.156.97/tc|/p2p/33w77YQLhgUt8HUJrMtntGGrs7RyXmot1of|mock-peer-9     |",
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

        self.mock_sad_path_miner = {
            "ota_version": "1.0.2.66",
            "region": "region_us915",
            "frequency_plan": "us915",
            "animal": "my-mocked-miner",
            "pubkey": "112YUf4TUQy4bxXRvGjrj6z7XyiSx8FDudTn6vtRYPgoGPnjBGWW",
            "miner": {
                "State": "not running",
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
            "miner_height": "1133539",
            "epoch": "30157",
            "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
            "ports": {
                "192.168.0.8:22": "open",
                "192.168.0.8:44158": "open",
                "33.117.96.28:22": "closed/timeout",
                "33.117.96.28:44158": "closed/timeout",
            },
            "private_ip": "192.168.0.8",
            "public_ip": "33.117.96.28",
            "peerbook": [
                "+-----------------------------------------------+--------------+----------+---------+---+----------+",
                "|                    address                    |     name     |listen_add|connectio|nat|last_updat|",
                "+-----------------------------------------------+--------------+----------+---------+---+----------+",
                "|/p2p/332YUS4TUQy4boXRvGjrj6z7XyiSx8FDxmTn6vtRYP|my-mock-miner |    1     |    7    |non| 293.353s |",
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
                "|/ip4/172.17.0.2/tc|/ip4/33.223.200.123/t|/p2p/2228k7YK3Ufah5qaAp37qe2jw3LaG6ycQUA|mock-peer-1     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.150.110.17/tc|/p2p/332qFc4yctCWyZyFaDhs4ve2ZsNEn1CKS1G|mock-peer-2     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.12.228.218/tc|/p2p/338eczMRVEBBeoCxiYjaZssdcHQXVk9Zokq|mock-peer-3     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.0.245.53/tcp/|/p2p/33Uyz1JBMcatg4SVYRRk2cxTz3tzvaKcFR7|mock-peer-4     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.37.13.24/tcp/|/p2p/33afuQSrmka2mgxLu91AdtDXbJ9wmqWBUxC|mock-peer-5     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.197.157.248/t|/p2p/33i6EevWXa6cskJepj8UnwMaKkPabZgK6QN|mock-peer-6     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.230.47.214/tc|/p2p/33sogMFP3m6Vgh2hsb3YCaRmG4GpyHdA1HH|mock-peer-7     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.68.166.175/tc|/p2p/33vTBsa1iXjy7QmFs6HFTSqK8ckSejQ3nwZ|mock-peer-8     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.238.156.97/tc|/p2p/33w77YQLhgUt8HUJrMtntGGrs7RyXmot1of|mock-peer-9     |",
                "+------------------+---------------------+----------------------------------------+----------------+",
                "",
                "",
            ],
            "height": ["30157    1148539", ""],
            "temp0": "65 °C",
            "temp1": "37 °C",
            "timestamp": "2021-12-21 18:18:39 +0000 UTC",
            "errors": "",
        }

        self.mock_speed = {
            "DownloadSpeed": "94 Mbit/s",
            "UploadSpeed": "57 Mbit/s",
            "Latency": "7.669083ms",
        }

    @patch("requests.get")
    def test_babcat_refresh_status(self, mock_requests_get):
        # assign
        b = Bobcat(self.mock_ip_address)

        # act
        b.refresh_status()

        # assert
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/status.json")

    @patch("requests.get")
    def test_babcat_refresh_miner(self, mock_requests_get):
        # assign
        b = Bobcat(self.mock_ip_address)

        # act
        b.refresh_miner()

        # assert
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/miner.json")

    @patch("requests.get")
    def test_babcat_refresh_speed(self, mock_requests_get):
        # assign
        b = Bobcat(self.mock_ip_address)

        # act
        b.refresh_speed()

        # assert
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/speed.json")

    @patch("requests.get")
    def test_babcat_refresh_dig(self, mock_requests_get):
        # assign
        b = Bobcat(self.mock_ip_address)

        # act
        b.refresh_dig()

        # assert
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/dig.json")

    @patch("requests.post")
    def test_babcat_resync(self, mock_requests_post):
        # assign
        b = Bobcat(self.mock_ip_address, self.mock_username, self.mock_password)

        # act
        _ = b.resync()

        # assert
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/resync",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    def test_babcat_reset(self, mock_requests_post):
        # assign
        b = Bobcat(self.mock_ip_address, self.mock_username, self.mock_password)

        # act
        _ = b.reset()

        # assert
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/reset",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    def test_babcat_reboot(self, mock_requests_post):
        # assign
        b = Bobcat(self.mock_ip_address, self.mock_username, self.mock_password)

        # act
        _ = b.reboot()

        # assert
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/reboot",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    def test_babcat_fastsync(self, mock_requests_post):
        # assign
        b = Bobcat(self.mock_ip_address, self.mock_username, self.mock_password)

        # act
        _ = b.fastsync()

        # assert
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/fastsync",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    def test_happy_path_babcat_is_healthy(
        self
    ):
        # assign
        b = Bobcat(self.mock_ip_address, self.mock_username, self.mock_password)
        b.status = self.mock_happy_path_status
        b.miner = self.mock_happy_path_miner

        # act
        result = b.is_healthy()

        # assert
        self.assertTrue(result)

    def test_sad_path_babcat_is_healthy(
        self
    ):
        # assign
        b = Bobcat(self.mock_ip_address, self.mock_username, self.mock_password)
        b.status = self.mock_sad_path_status
        b.miner = self.mock_sad_path_miner

        # act
        result = b.is_healthy()

        # assert
        self.assertFalse(result)

    def test_babcat_is_relayed(self):
        # assign
        b = Bobcat(self.mock_ip_address, self.mock_username, self.mock_password)
        b.miner = self.mock_happy_path_miner

        # act
        result = b.is_relayed()

        # assert
        self.assertFalse(result)

    def test_babcat_has_errors(self):
        # assign
        b = Bobcat(self.mock_ip_address)
        b.miner = self.mock_happy_path_miner

        # act
        result = b.has_errors()

        # assert
        self.assertEqual(result, False)

    def test_babcat_should_fastsync(self):
        # assign
        b = Bobcat(self.mock_ip_address)
        b.status = self.mock_happy_path_status
        b.miner = self.mock_happy_path_miner

        # act
        result = b.should_fastsync()

        # assert
        self.assertEqual(result, False)

    def test_babcat_should_resync(self):
        # assign
        b = Bobcat(self.mock_ip_address)
        b.status = self.mock_happy_path_status
        b.miner = self.mock_happy_path_miner

        # act
        result = b.should_resync()

        # assert
        self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
