"""Unittests for bobcat REST API."""
from unittest.mock import patch, call

import unittest
import requests

from bobcat_miner import Bobcat

import mock_bobcat 


class TestBobcat(unittest.TestCase):

    def setUp(self):
        self.mock_ip_address = "x.x.x.x"

    @patch("requests.get")
    def test_babcat_refresh_status(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.refresh_status()
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/status.json")

    @patch("requests.get")
    def test_babcat_refresh_miner(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.refresh_miner()
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/miner.json")

    @patch("requests.get")
    def test_babcat_refresh_speed(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.refresh_speed()
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/speed.json")

    @patch("requests.get")
    def test_babcat_refresh_dig(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.refresh_dig()
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address + "/dig.json")
    
    @patch("requests.get")
    def test_babcat_refresh(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.refresh()
        mock_requests_get.assert_has_calls(
            [
                call('http://' + self.mock_ip_address + '/status.json'),
                call('http://' + self.mock_ip_address + '/miner.json'),
                call('http://' + self.mock_ip_address + '/speed.json'),
                call('http://' + self.mock_ip_address + '/dig.json')
            ],
            any_order=True,
        )

    @patch("requests.post")
    def test_babcat_resync(self, mock_requests_post):
        b = Bobcat(self.mock_ip_address)
        _ = b.resync()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/resync",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    def test_babcat_reset(self, mock_requests_post):
        b = Bobcat(self.mock_ip_address)
        _ = b.reset()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/reset",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    def test_babcat_reboot(self, mock_requests_post):
        b = Bobcat(self.mock_ip_address)
        _ = b.reboot()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/reboot",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("requests.post")
    def test_babcat_fastsync(self, mock_requests_post):
        b = Bobcat(self.mock_ip_address)
        _ = b.fastsync()
        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_ip_address + "/admin/fastsync",
            header={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )
    
    @patch("requests.get")
    def test_babcat_can_connect(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        b.can_connect()
        mock_requests_get.assert_called_once_with("http://" + self.mock_ip_address)
    
    @patch("requests.get", side_effect=Exception)
    def test_babcat_throws_error_when_cannot_connect(self, mock_requests_get):
        b = Bobcat(self.mock_ip_address)
        self.assertRaises(Exception, Bobcat(self.mock_ip_address))


class TestSyncedBobcat(unittest.TestCase):

    @patch("requests.get", side_effect=mock_bobcat.mock_synced_bobcat)
    def setUp(self, mock_requests_get):
        self.bobcat = Bobcat("x.x.x.x")
        self.bobcat.refresh()
    
    def test_babcat_is_running(self):
        self.assertTrue(self.bobcat.is_running())
    
    def test_babcat_is_synced(self):
        self.assertTrue(self.bobcat.is_synced())

    def test_babcat_is_temp_safe(self):
        self.assertTrue(self.bobcat.is_temp_safe())

    def test_babcat_has_errors(self):
        self.assertFalse(self.bobcat.has_errors())
    
    def test_babcat_is_healthy(self):
        self.assertTrue(self.bobcat.is_healthy())

    def test_babcat_is_relayed(self):
        self.assertFalse(self.bobcat.is_relayed())

    def is_local_network_slow(self):
        self.assertFalse(self.bobcat.is_local_network_slow())

    def test_babcat_should_fastsync(self):
        self.assertFalse(self.bobcat.should_fastsync())
    
    def test_babcat_should_resync(self):
        self.assertFalse(self.bobcat.should_resync())


class TestUnsyncedBobcat(unittest.TestCase):
    @patch("requests.get", side_effect=mock_bobcat.mock_unsynced_bobcat)    
    def setUp(self, mock_requests_get):
        self.bobcat = Bobcat("x.x.x.x")
        self.bobcat.refresh()
    
    def test_babcat_is_synced(self):
        self.assertFalse(self.bobcat.is_synced())

    def test_babcat_is_healthy(self):
        self.assertFalse(self.bobcat.is_healthy())
    
    def is_local_network_slow(self):
        self.assertTrue(self.bobcat.is_local_network_slow())

    def test_babcat_should_fastsync(self):
        self.assertTrue(self.bobcat.should_fastsync())
    
    def test_babcat_should_resync(self):
        self.assertFalse(self.bobcat.should_resync())
    
    def test_babcat_should_reboot(self):
        self.assertTrue(self.bobcat.should_reboot())
    
    def test_babcat_should_reset(self):
        self.assertFalse(self.bobcat.should_reset())


class TestUnhealthyBobcat(unittest.TestCase):
    @patch("requests.get", side_effect=mock_bobcat.mock_unhealthy_bobcat)
    def setUp(self, mock_requests_get):
        self.bobcat = Bobcat("x.x.x.x")
        self.bobcat.refresh()
    
    def test_babcat_is_running(self):
        self.assertFalse(self.bobcat.is_running())
    
    def test_babcat_is_synced(self):
        self.assertFalse(self.bobcat.is_synced())

    def test_babcat_is_temp_safe(self):
        self.assertFalse(self.bobcat.is_temp_safe())

    def test_babcat_has_errors(self):
        self.assertTrue(self.bobcat.has_errors())
    
    def test_babcat_is_healthy(self):
        self.assertFalse(self.bobcat.is_healthy())

    def test_babcat_is_relayed(self):
        self.assertTrue(self.bobcat.is_relayed())

    def test_babcat_should_fastsync(self):
        self.assertFalse(self.bobcat.should_fastsync())
    
    def test_babcat_should_resync(self):
        self.assertTrue(self.bobcat.should_resync())
    
    def test_babcat_should_reboot(self):
        self.assertTrue(self.bobcat.should_reboot())
    
    def test_babcat_should_reset(self):
        self.assertTrue(self.bobcat.should_reset())


if __name__ == "__main__":
    unittest.main()
