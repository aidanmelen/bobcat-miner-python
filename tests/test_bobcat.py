"""Unittests for bobcat REST API."""
from unittest.mock import patch
from unittest.mock import call
from unittest.mock import MagicMock

import datetime
import unittest
import requests

from bobcat_miner import Bobcat
from bobcat_miner import BobcatConnection
from bobcat_miner import BobcatLogger
from bobcat_miner import BobcatConnectionError

import mock_bobcat


DISABLED = 100


class TestBobcatAPI(unittest.TestCase):
    """Test BobcatAPI."""

    def setUp(self):
        self.mock_hostname = "192.168.0.10"

    @patch("requests.get")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat")
    def test_refresh_status(self, mock_is_a_bobcat, mock_requests_get):
        mock_is_a_bobcat.return_value = self.mock_hostname
        b = Bobcat(hostname=self.mock_hostname, log_level=DISABLED)
        b.refresh_status()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/status.json")

    @patch("requests.get")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat")
    def test_refresh_miner(self, mock_is_a_bobcat, mock_requests_get):
        mock_is_a_bobcat.return_value = self.mock_hostname
        b = Bobcat(hostname=self.mock_hostname, log_level=DISABLED)
        b.refresh_miner()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/miner.json")

    @patch("requests.get")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat")
    def test_refresh_temp(self, mock_is_a_bobcat, mock_requests_get):
        mock_is_a_bobcat.return_value = self.mock_hostname
        b = Bobcat(hostname=self.mock_hostname, log_level=DISABLED)
        b.refresh_temp()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/temp.json")

    @patch("requests.get")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat")
    def test_refresh_speed(self, mock_is_a_bobcat, mock_requests_get):
        mock_is_a_bobcat.return_value = self.mock_hostname
        b = Bobcat(hostname=self.mock_hostname, log_level=DISABLED)
        b.refresh_speed()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/speed.json")

    @patch("requests.get")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat")
    def test_refresh_dig(self, mock_is_a_bobcat, mock_requests_get):
        mock_is_a_bobcat.return_value = self.mock_hostname
        b = Bobcat(hostname=self.mock_hostname, log_level=DISABLED)
        b.refresh_dig()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/dig.json")

    @patch("requests.get")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat")
    def test_refresh(self, mock_is_a_bobcat, mock_requests_get):
        mock_is_a_bobcat.return_value = self.mock_hostname
        b = Bobcat(hostname=self.mock_hostname, log_level=DISABLED)
        b.refresh()
        mock_requests_get.assert_has_calls(
            [
                call("http://" + self.mock_hostname + "/status.json"),
                call("http://" + self.mock_hostname + "/miner.json"),
                call("http://" + self.mock_hostname + "/temp.json"),
                call("http://" + self.mock_hostname + "/speed.json"),
                call("http://" + self.mock_hostname + "/dig.json"),
            ],
            any_order=True,
        )

    @patch("requests.post")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat")
    def test_reboot(self, mock_is_a_bobcat, mock_requests_post):
        mock_is_a_bobcat.return_value = self.mock_hostname
        b = Bobcat(hostname=self.mock_hostname, log_level=DISABLED)
        _ = b.reboot()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/reboot",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat")
    def test_reset(self, mock_is_a_bobcat, mock_requests_post):
        mock_is_a_bobcat.return_value = self.mock_hostname
        b = Bobcat(hostname=self.mock_hostname, log_level=DISABLED)
        _ = b.reset()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/reset",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat")
    def test_resync(self, mock_is_a_bobcat, mock_requests_post):
        mock_is_a_bobcat.return_value = self.mock_hostname
        b = Bobcat(hostname=self.mock_hostname, log_level=DISABLED)
        _ = b.resync()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/resync",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat")
    def test_fastsync(self, mock_is_a_bobcat, mock_requests_post):
        mock_is_a_bobcat.return_value = self.mock_hostname
        b = Bobcat(hostname=self.mock_hostname, log_level=DISABLED)
        _ = b.fastsync()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/fastsync",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )


class TestBobcat(unittest.TestCase):
    """Test Bobcat."""

    @patch("requests.get", side_effect=mock_bobcat.mock_synced_bobcat)
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat")
    def setUp(self, mock_is_a_bobcat, mock_requests_get):
        mock_is_a_bobcat.return_value = "192.168.0.10"
        self.bobcat = Bobcat("192.168.0.10")
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

    def test_tip(self):
        self.assertEqual(self.bobcat.tip, None)

    def test_ota_version(self):
        self.assertEqual(self.bobcat.ota_version, "1.0.2.66")

    def test_region(self):
        self.assertEqual(self.bobcat.region, "region_us915")

    def test_frequency_plan(self):
        self.assertEqual(self.bobcat.frequency_plan, "us915")

    def test_animal(self):
        self.assertEqual(self.bobcat.animal, "fancy-awesome-bobcat")

    def test_name(self):
        self.assertEqual(self.bobcat.name, "Fancy Awesome Bobcat")

    def test_pubkey(self):
        self.assertEqual(
            self.bobcat.pubkey,
            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        )

    def test_state(self):
        self.assertEqual(self.bobcat.state, "running")

    def test_miner_status(self):
        self.assertEqual(self.bobcat.miner_status, "Up 36 hours")

    def test_names(self):
        self.assertEqual(self.bobcat.names, ["/miner"])

    def test_image(self):
        self.assertEqual(
            self.bobcat.image,
            "quay.io/team-helium/miner:miner-arm64_2021.12.14.0_GA",
        )

    def test_created(self):
        self.assertEqual(self.bobcat.created, 1639980913)

    def test_p2p_status(self):
        self.assertTrue("|connected|  yes  |" in self.bobcat.p2p_status)
        self.assertTrue("|dialable |  yes  |" in self.bobcat.p2p_status)
        self.assertTrue("|nat_type | none  |" in self.bobcat.p2p_status)
        self.assertTrue("| height  |1148539|" in self.bobcat.p2p_status)

    def test_ports_desc(self):
        self.assertEqual(
            self.bobcat.ports_desc,
            "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
        )

    def test_ports(self):
        self.assertEqual(
            self.bobcat.ports,
            {
                "192.168.0.10:22": "open",
                "192.168.0.10:44158": "open",
                "33.117.96.28:22": "closed/timeout",
                "33.117.96.28:44158": "closed/timeout",
            },
        )

    def test_private_ip(self):
        self.assertEqual(self.bobcat.private_ip, "192.168.0.10")

    def test_public_ip(self):
        self.assertEqual(self.bobcat.public_ip, "33.117.96.28")

    def test_peerbook(self):
        self.assertTrue(
            "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    1     |    7    |non| 293.353s |"
            in self.bobcat.peerbook
        )
        self.assertTrue("|/ip4/33.117.96.28/tcp/44158|" in self.bobcat.peerbook)
        self.assertTrue(
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|"
            in self.bobcat.peerbook
        )

    def test_timestamp(self):
        self.assertEqual(
            self.bobcat.timestamp,
            "2021-12-21 18:18:39 +0000 UTC",
        )

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
                {"A": "54.232.171.76", "dial": "success", "ttl": 16},
                {"A": "13.211.2.73", "dial": "success", "ttl": 16},
                {"A": "3.15.87.218", "dial": "success", "ttl": 16},
            ],
        )


if __name__ == "__main__":
    unittest.main()
