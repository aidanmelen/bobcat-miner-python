"""Unittests for bobcat REST API."""
from unittest.mock import patch, call, PropertyMock

import unittest
import requests

from bobcat_miner import Bobcat, Autopilot

import mock_bobcat


class TestAutopilotDiagnose(unittest.TestCase):
    @patch("requests.get", side_effect=mock_bobcat.mock_synced_bobcat)
    def setUp(self, mock_requests_get):
        bobcat = Bobcat("x.x.x.x")
        bobcat.refresh()
        self.autopilot = Autopilot(bobcat)

    def test_is_relayed(self):
        self.assertFalse(self.autopilot.is_relayed)

    def test_is_temp_safe(self):
        self.assertTrue(self.autopilot.is_temp_safe)

    def test_is_local_network_slow(self):
        self.assertFalse(self.autopilot.is_local_network_slow)


class TestAutopilotActions(unittest.TestCase):
    @patch("requests.get", side_effect=mock_bobcat.mock_synced_bobcat)
    def setUp(self, mock_requests_get):
        bobcat = Bobcat("x.x.x.x")
        bobcat.refresh()
        self.autopilot = Autopilot(bobcat)

    @patch("bobcat_miner.Bobcat.ping", side_effect=[False, False, True])
    @patch("time.sleep", return_value=None)
    def test_wait(self, mock_time_sleep, mock_bobcat_ping):
        self.autopilot.wait()
        mock_time_sleep.assert_has_calls(
            [call(300), call(60)],  # FIVE_MINUTES  # ONE_MINUTE
            any_order=False,
        )
        self.assertEqual(mock_bobcat_ping.call_count, 3)

    # @patch("bobcat_miner.Bobcat.refresh_status")
    # @patch("bobcat_miner.Bobcat.gap")
    # @patch("time.sleep", return_value=None)
    # def test_is_gap_growing(self, mock_time_sleep, mock_bobcat_gap, mock_bobcat_refresh_status):

    #     mock_bobcat_gap = PropertyMock(side_effect=[600, 700, 600, 700, 800, 900])
    #     self.autopilot.is_gap_growing()


if __name__ == "__main__":
    unittest.main()
