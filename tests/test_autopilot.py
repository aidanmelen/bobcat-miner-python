"""Unittests for bobcat REST API."""
from unittest.mock import patch, call, PropertyMock

import logging
import unittest
import requests

from bobcat_miner import Bobcat, Autopilot

import mock_bobcat


class TestAutopilotDiagnoseHealthyBobcat(unittest.TestCase):
    """Test Autopilot diagnosing an healthy Bobcat"""

    @patch("requests.get", side_effect=mock_bobcat.mock_synced_bobcat)
    def setUp(self, mock_requests_get):
        bobcat = Bobcat("x.x.x.x")
        bobcat.refresh()
        self.autopilot = Autopilot(bobcat, log_file=None, log_level="NOTSET")
        logging.getLogger("bobcat-autopilot").disabled = True

    def test_is_relayed(self):
        self.assertFalse(self.autopilot.is_relayed())

    def test_is_temp_dangerous(self):
        self.assertFalse(self.autopilot.is_temp_dangerous())

    def test_is_network_speed_slow(self):
        self.assertFalse(self.autopilot.is_network_speed_slow())

    def test_has_errors(self):
        self.assertFalse(self.autopilot.has_errors())


class TestAutopilotDiagnoseUnhealthyBobcat(unittest.TestCase):
    """Test Autopilot diagnosing an unhealthy Bobcat"""

    @patch("requests.get", side_effect=mock_bobcat.mock_unhealthy_bobcat)
    def setUp(self, mock_requests_get):
        bobcat = Bobcat("x.x.x.x")
        bobcat.refresh()
        self.autopilot = Autopilot(bobcat, log_file=None, log_level="NOTSET")
        logging.getLogger("bobcat-autopilot").disabled = True

    def test_is_relayed(self):
        self.assertTrue(self.autopilot.is_relayed())

    def test_is_temp_dangerous(self):
        self.assertTrue(self.autopilot.is_temp_dangerous())

    def test_is_network_speed_slow(self):
        self.assertTrue(self.autopilot.is_network_speed_slow())

    def test_has_errors(self):
        self.assertTrue(self.autopilot.has_errors())


class TestAutopilotActions(unittest.TestCase):
    """Test Autopilot actions"""

    @patch("requests.get", side_effect=mock_bobcat.mock_synced_bobcat)
    def setUp(self, mock_requests_get):
        bobcat = Bobcat("x.x.x.x")
        bobcat.refresh()
        self.autopilot = Autopilot(bobcat, log_file=None, log_level="NOTSET")
        logging.getLogger("bobcat-autopilot").disabled = True

    @patch("bobcat_miner.Autopilot._wait_for_loading")
    @patch("bobcat_miner.Bobcat.ping", side_effect=[False, False, True])
    @patch("time.sleep", return_value=None)
    def test_wait(self, mock_time_sleep, mock_bobcat_ping, mock_autopilot_wait_for_loading):
        self.autopilot.wait()
        mock_time_sleep.assert_has_calls(
            [call(Autopilot.THIRTY_MINUTES), call(Autopilot.FIVE_MINUTES)],
            any_order=False,
        )
        self.assertEqual(mock_bobcat_ping.call_count, 3)
        self.assertTrue(mock_autopilot_wait_for_loading.called_once_with(Autopilot.TEN_MINUTES))


if __name__ == "__main__":
    unittest.main()
