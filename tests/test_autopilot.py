from unittest.mock import patch, call, PropertyMock, AsyncMock, MagicMock

import unittest

from bobcat_miner import BobcatAutopilot, OnlineStatusCheck, SyncStatusCheck, RelayStatusCheck

import mock_endpoints


class TestAutopilot(unittest.TestCase):
    """Test BobcatAutopilot."""

    @patch("bobcat_miner.BobcatAutopilot.checks", new_callable=PropertyMock)
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.post")
    @patch("requests.get", side_effect=mock_endpoints.mock_synced_bobcat)
    def setUp(self, mock_requests_get, mock_requests_post, mock_verify, mock_checks):
        self.mock_hostname = "192.168.0.10"
        self.autopilot = BobcatAutopilot(hostname=self.mock_hostname)
        self.autopilot.refresh()
        self.autopilot._logger = MagicMock()
        # self.mock_checks

    @patch("bobcat_miner.Bobcat.fastsync")
    @patch("bobcat_miner.Bobcat.resync")
    @patch("bobcat_miner.Bobcat.reset")
    @patch("bobcat_miner.Bobcat.reboot")
    @patch("filelock.FileLock")
    def test_run(self, mock_filelock, mock_reboot, mock_reset, mock_resync, mock_fastsync):
        self.autopilot.run()
        self.autopilot._logger.assert_has_calls(
            [
                call.debug("The Bobcat Autopilot is starting 🚀 🚀 🚀"),
                call.debug("Lock Acquired: .bobcat.lock"),
                call.debug("Checking: Online Status"),
                call.warning(
                    "Online Status: Bobcat is running and the Helium API is stale", extra={}
                ),
                call.debug("Checking: Sync Status"),
                call.info("Sync Status: Synced (gap:0) 💫"),
                call.debug("Checking: Relay Status"),
                call.info("Relay Status: Not Relayed ✨"),
                call.debug("Checking: Network Status"),
                call.info("Network Status: Good 📶"),
                call.debug("Checking: Temperature Status"),
                call.info("Temperature Status: Good (38°C) ☀️"),
                call.debug("Checking: OTA Version Change"),
                call.debug("Checking: Down or Error Status"),
                call.debug("Checking: Height API Error Status"),
                call.debug("Lock Released: .bobcat.lock"),
                call.debug("The Bobcat Autopilot is finished ✨ 🍰 ✨"),
            ],
            any_order=False,
        )


if __name__ == "__main__":
    unittest.main()
