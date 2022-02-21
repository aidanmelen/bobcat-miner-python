from unittest.mock import patch, call, PropertyMock, AsyncMock, MagicMock, mock_open

import unittest

from bobcat_miner import BobcatAutopilot, Bobcat, OnlineStatusCheck

import mock_endpoints


class TestAutopilot(unittest.TestCase):
    """Test BobcatAutopilot."""

    @patch("bobcat_miner.BobcatAutopilot.error_checks", new_callable=PropertyMock)
    @patch("bobcat_miner.BobcatAutopilot.status_checks", new_callable=PropertyMock)
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.post")
    @patch("requests.get", side_effect=mock_endpoints.mock_online)
    def setUp(
        self,
        mock_requests_get,
        mock_requests_post,
        mock_verify,
        mock_status_checks,
        mock_error_checks,
    ):
        self.mock_hostname = "192.168.0.10"
        self.bobcat = Bobcat(hostname=self.mock_hostname)
        self.bobcat.logger = MagicMock()
        self.bobcat.refresh()
        mock_lock_file = ".mock.lock"
        mock_state_file = ".mock.json"
        mock_verbose = False
        self.autopilot = BobcatAutopilot(self.bobcat, mock_lock_file, mock_state_file, mock_verbose)

    @patch("bobcat_miner.Bobcat.fastsync")
    @patch("bobcat_miner.Bobcat.resync")
    @patch("bobcat_miner.Bobcat.reset")
    @patch("bobcat_miner.Bobcat.reboot")
    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open, read_data='{"ota_version": "1.0.2.76"}')
    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=True)
    @patch("filelock.FileLock.acquire")
    def test_run(
        self,
        mock_filelock,
        mock_os_path_isfile,
        mock_os_path_exists,
        mock_open,
        mock_json_dump,
        mock_reboot,
        mock_reset,
        mock_resync,
        mock_fastsync,
    ):
        self.autopilot.run()
        self.bobcat.logger.assert_has_calls(
            [
                call.debug("Refresh: Status Data"),
                call.debug("Refresh: Miner Data"),
                call.debug("Refresh: Network Speed Data"),
                call.debug("Refresh: Temperature Data"),
                call.debug("Refresh: DNS Data"),
                call.debug("The Bobcat Autopilot is starting 🚀 🚀 🚀"),
                call.debug("Lock Acquired: .mock.lock"),
                call.warning(
                    "Online Status: Bobcat is healthy. Helium API needs time to update.", extra={}
                ),
                call.debug("Checking: Down or Error Status"),
                call.debug("Checking: Height API Error Status"),
                call.debug("Checking: Unknown Error Status"),
                call.debug("Checking: Sync Status"),
                call.info("Sync Status: Synced (gap:0) 💫"),
                call.debug("Checking: Relay Status"),
                call.info("Relay Status: Not Relayed ✨"),
                call.debug("Checking: Network Status"),
                call.info("Network Status: Good 📶"),
                call.debug("Checking: Temperature Status"),
                call.info("Temperature Status: Good (38°C) ☀️"),
                call.debug("Checking: OTA Version Change"),
                call.debug("Lock Released: .mock.lock"),
                call.debug("The Bobcat Autopilot is finished ✨ 🍰 ✨"),
            ],
            any_order=False,
        )


if __name__ == "__main__":
    unittest.main()
