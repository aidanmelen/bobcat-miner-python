"""Unittests for bobcat REST API."""
from unittest.mock import patch, call

import datetime
import unittest
import requests

from bobcat_miner import Bobcat

import mock_bobcat 


class TestBobcatAPI(unittest.TestCase):

    def setUp(self):
        self.mock_ip_address = "x.x.x.x"

    @patch("requests.get")
    def test_refresh_status(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.refresh_status()
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/status.json")

    @patch("requests.get")
    def test_refresh_miner(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.refresh_miner()
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/miner.json")
    
    @patch("requests.get")
    def test_refresh_temp(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.refresh_temp()
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/temp.json")

    @patch("requests.get")
    def test_refresh_speed(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.refresh_speed()
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/speed.json")

    @patch("requests.get")
    def test_refresh_dig(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.refresh_dig()
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/dig.json")
    
    @patch("requests.get")
    def test_refresh(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.refresh()
        mock_requests_get.assert_has_calls(
            [
                call('http://' + self.mock_ip_address + '/status.json'),
                call('http://' + self.mock_ip_address + '/miner.json'),
                call('http://' + self.mock_ip_address + '/temp.json'),
                call('http://' + self.mock_ip_address + '/speed.json'),
                call('http://' + self.mock_ip_address + '/dig.json')
            ],
            any_order=True,
        )
    
    @patch("requests.post")
    def test_reboot(self, mock_requests_post):
        b = Bobcat(self.mock_ip_address)
        _ = b.reboot()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/reboot",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    def test_reset(self, mock_requests_post):
        b = Bobcat(self.mock_ip_address)
        _ = b.reset()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/reset",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    def test_resync(self, mock_requests_post):
        b = Bobcat(self.mock_ip_address)
        _ = b.resync()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/resync",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    def test_fastsync(self, mock_requests_post):
        b = Bobcat(self.mock_ip_address)
        _ = b.fastsync()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/fastsync",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )


class TestBobcatProperties(unittest.TestCase):

    @patch("requests.get", side_effect=mock_bobcat.mock_synced_bobcat)
    def setUp(self, mock_requests_get):
        self.bobcat = Bobcat("x.x.x.x")
        self.bobcat.refresh()
    
    def test_status(self):
        self.assertEqual(self.bobcat.status, "Synced")

    def test_gap(self):
        self.assertEqual(self.bobcat.gap, 0)

    def test_miner_height(self):
        self.assertEqual(self.bobcat.miner_height, 1148539)

    def test_blockchain_height(self):
        self.assertEqual(self.bobcat.blockchain_height, 1148539)

    def test_epoch(self):
        self.assertEqual(self.bobcat.epoch, 30157)

    def test_ota_version(self):
        self.assertEqual(self.bobcat.ota_version, "1.0.2.66")

    def test_region(self):
        self.assertEqual(self.bobcat.region, "region_us915")

    def test_frequency_plan(self):
        self.assertEqual(self.bobcat.frequency_plan, "us915")

    def test_animal(self):
        self.assertEqual(self.bobcat.animal, "my-mocked-miner")

    def test_name(self):
        self.assertEqual(self.bobcat.name, "My Mocked Miner")

    def test_pubkey(self):
        self.assertEqual(self.bobcat.pubkey, "112YUf4TUQy4bxXRvGjrj6z7XyiSx8FDudTn6vtRYPgoGPnjBGWW")

    def test_state(self):
        self.assertEqual(self.bobcat.state, "running")
    
    def test_miner_status(self):
        self.assertEqual(self.bobcat.miner_status, "Up 36 hours")

    def test_names(self):
        self.assertEqual(self.bobcat.names, ["/miner"])

    def test_image(self):
        self.assertEqual(self.bobcat.image, "quay.io/team-helium/miner:miner-arm64_2021.12.14.0_GA")

    def test_created(self):
        self.assertEqual(self.bobcat.created, datetime.datetime(2021, 12, 20, 6, 15, 13))

    def test_p2p_status(self):
        self.assertEqual(
            self.bobcat.p2p_status,
            {
                'connected': 'yes', 
                'dialable': 'yes', 
                'nat_type': 'none', 
                'height': '1148539'
            }
        )

    def test_ports_desc(self):
        self.assertEqual(self.bobcat.ports_desc, "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK")

    def test_ports(self):
        self.assertEqual(
            self.bobcat.ports,
            {
                "192.168.0.8:22": "open",
                "192.168.0.8:44158": "open",
                "33.117.96.28:22": "closed/timeout",
                "33.117.96.28:44158": "closed/timeout",
            }
        )

    def test_private_ip(self):
        self.assertEqual(self.bobcat.private_ip, "192.168.0.8")

    def test_public_ip(self):
        self.assertEqual(self.bobcat.public_ip, "33.117.96.28")

    def test_peerbook(self):
        self.assertEqual(
            self.bobcat.peerbook,
            [
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
            ]
        )

    def test_listen_address(self):
        self.assertEqual(self.bobcat.listen_address, "/ip4/33.117.96.28/tcp/44158")

    def test_timestamp(self):
        self.assertEqual(self.bobcat.timestamp, datetime.datetime(2021, 12, 21, 18, 18, 39, tzinfo=datetime.timezone(datetime.timedelta(0), 'UTC')))

    def test_error(self):
        self.assertEqual(self.bobcat.error, None)

    def test_temp0(self):
        self.assertEqual(self.bobcat.temp0, 38)

    def test_temp1(self):
        self.assertEqual(self.bobcat.temp1, 37)

    def test_temp0_c(self):
        self.assertEqual(self.bobcat.temp0_c, 38)

    def test_temp1_c(self):
        self.assertEqual(self.bobcat.temp1_c, 37)

    def test_temp0_f(self):
        self.assertEqual(self.bobcat.temp0_f, 100.4)

    def test_temp1_f(self):
        self.assertEqual(self.bobcat.temp1_f, 98.6)

    def test_download_speed(self):
        self.assertEqual(self.bobcat.download_speed, "94 Mbit/s")

    def test_upload_speed(self):
        self.assertEqual(self.bobcat.upload_speed, "57 Mbit/s")

    def test_latency(self):
        self.assertEqual(self.bobcat.latency, "7.669083ms")

    def test_dig_name(self):
        self.assertEqual(self.bobcat.dig_name, "seed.helium.io.")

    def test_dig_message(self):
        self.assertEqual(self.bobcat.dig_message, None)

    def test_dig_dns(self):
        self.assertEqual(self.bobcat.dig_dns, "Local DNS")

    def test_dig_records(self):
        self.assertEqual(
            self.bobcat.dig_records,
            [
                {
                    "A": "54.232.171.76",
                    "dial": "success",
                    "ttl": 16
                },
                {
                    "A": "13.211.2.73",
                    "dial": "success",
                    "ttl": 16
                },
                {
                    "A": "3.15.87.218",
                    "dial": "success",
                    "ttl": 16
                }
            ]
        )

    def test_is_running(self):
        self.assertTrue(self.bobcat.is_running)

    def test_is_synced(self):
        self.assertTrue(self.bobcat.is_synced)

    def test_is_loading(self):
        self.assertFalse(self.bobcat.is_loading)

    def test_is_relayed(self):
        self.assertFalse(self.bobcat.is_relayed)

    def test_is_temp_safe(self):
        self.assertTrue(self.bobcat.is_temp_safe)

    def test_is_local_network_slow(self):
        self.assertFalse(self.bobcat.is_local_network_slow)



# class TestSyncedBobcat(unittest.TestCase):

#     @patch("requests.get", side_effect=mock_bobcat.mock_synced_bobcat)
#     def setUp(self, mock_requests_get):
#         self.bobcat = Bobcat("x.x.x.x")
#         self.bobcat.refresh()
    
#     def test_is_synced(self):
#         self.assertTrue(self.bobcat.is_synced)

#     def test_is_running(self):
#         self.assertTrue(self.bobcat.is_running)

#     def test_is_temp_safe(self):
#         self.assertTrue(self.bobcat.is_temp_safe)

#     def test_is_relayed(self):
#         self.assertFalse(self.bobcat.is_relayed)

#     def is_local_network_slow(self):
#         self.assertFalse(self.bobcat.is_local_network_slow)


# class TestUnsyncedBobcat(unittest.TestCase):
#     @patch("requests.get", side_effect=mock_bobcat.mock_unsynced_bobcat)    
#     def setUp(self, mock_requests_get):
#         self.bobcat = Bobcat("x.x.x.x")
#         self.bobcat.refresh()

#     def test_is_synced(self):
#         self.assertFalse(self.bobcat.is_synced)
    
#     def test_is_running(self):
#         self.assertFalse(self.bobcat.is_running)
    
#     def is_local_network_slow(self):
#         self.assertTrue(self.bobcat.is_local_network_slow)


# class TestUnhealthyBobcat(unittest.TestCase):
#     @patch("requests.get", side_effect=mock_bobcat.mock_unhealthy_bobcat)
#     def setUp(self, mock_requests_get):
#         self.bobcat = Bobcat("x.x.x.x")
#         self.bobcat.refresh()
    
#     def test_is_running(self):
#         self.assertFalse(self.bobcat.is_running)
    
#     def test_is_synced(self):
#         self.assertFalse(self.bobcat.is_synced)

#     def test_is_temp_safe(self):
#         self.assertFalse(self.bobcat.is_temp_safe)

#     def test_is_relayed(self):
#         self.assertTrue(self.bobcat.is_relayed)


if __name__ == "__main__":
    unittest.main()
