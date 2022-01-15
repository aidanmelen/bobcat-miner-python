"""Unittests for bobcat REST API."""
from unittest.mock import patch, call, PropertyMock

import logging
import unittest
import requests

from bobcat_miner import Bobcat, Autopilot

import mock_bobcat


class TestAutopilotDiagnose(unittest.TestCase):
    @patch("requests.get", side_effect=mock_bobcat.mock_synced_bobcat)
    def setUp(self, mock_requests_get):
        bobcat = Bobcat("x.x.x.x")
        bobcat.refresh()
        self.autopilot = Autopilot(bobcat, log_file=None, log_level=logging.NOTSET)

    def test_diagnose_relay(self):
        self.assertFalse(self.autopilot.diagnose_relay())

    def test_diagnose_temp(self):
        self.assertTrue(self.autopilot.diagnose_temp())

    def test_diagnose_network_speed(self):
        self.assertFalse(self.autopilot.diagnose_network_speed())


class TestAutopilotActions(unittest.TestCase):
    @patch("requests.get", side_effect=mock_bobcat.mock_synced_bobcat)
    def setUp(self, mock_requests_get):
        bobcat = Bobcat("x.x.x.x")
        bobcat.refresh()
        self.autopilot = Autopilot(bobcat, log_file=None, log_level=logging.NOTSET)

    @patch("bobcat_miner.Autopilot._wait_loading")
    @patch("bobcat_miner.Bobcat.ping", side_effect=[False, False, True])
    @patch("time.sleep", return_value=None)
    def test_wait(self, mock_time_sleep, mock_bobcat_ping, mock_autopilot_wait_loading):
        self.autopilot.wait()
        mock_time_sleep.assert_has_calls(
            [call(Autopilot.THIRTY_MINUTES), call(Autopilot.FIVE_MINUTES)],
            any_order=False,
        )
        self.assertEqual(mock_bobcat_ping.call_count, 3)
        self.assertTrue(
            mock_autopilot_wait_loading.called_once_with(
                Autopilot.THIRTY_MINUTES, Autopilot.FIVE_MINUTES
            )
        )


#     # @patch("bobcat_miner.Bobcat.refresh_status")
#     # @patch("bobcat_miner.Bobcat.gap")
#     # @patch("time.sleep", return_value=None)
#     # def test_is_gap_growing(self, mock_time_sleep, mock_bobcat_gap, mock_bobcat_refresh_status):

#     #     mock_bobcat_gap = PropertyMock(side_effect=[600, 700, 600, 700, 800, 900])
#     #     self.autopilot.is_gap_growing()


if __name__ == "__main__":
    unittest.main()
