from unittest.mock import MagicMock, patch, call, mock_open

import unittest

from bobcat_miner import BobcatDiagnoser


class TestBobcatDiagnoser(unittest.TestCase):
    """Test BobcatDiagnoser."""

    def test_check_error(self):
        d = BobcatDiagnoser()
        d._logger = MagicMock()
        d.status = "Error"
        d.tip = " Error response from daemon: Container 49dd5fae6f3094e240e9aa339947bc9f6336d5f997c495a37696095fc306f3d1 is restarting, wait until the container is running exit status 1"
        self.assertTrue(d.check_down_or_error())
        d.status = "Synced"
        d.tip = ""
        self.assertFalse(d.check_down_or_error())

    def test_check_down(self):
        d = BobcatDiagnoser()
        d._logger = MagicMock()
        d.status = "Down"
        self.assertTrue(d.check_down_or_error())
        d.status = "Synced"
        self.assertFalse(d.check_down_or_error())

    def test_check_height_api_error(self):
        d = BobcatDiagnoser()
        d._logger = MagicMock()
        d.status = "Height API Error"
        self.assertTrue(d.check_height_api_error())
        d.status = "Synced"
        self.assertFalse(d.check_height_api_error())

    # def test_check_no_activity_issue(self):
    #     pass

    # def test_check_no_witness_issue(self):
    #     pass

    # def test_check_block_checksum_mismatch_error(self):
    #     pass

    # def test_check_compression_method_or_corrupted_error(self):
    #     pass

    # def test_check_too_many_lookup_attempts_error(self):
    #     pass

    # def test_check_oboarding_dewi_org_nxdomain_error(self):
    #     pass

    # def test_check_failed_to_start_child_error(self):
    #     pass

    # def test_check_not_a_dets_file_error(self):
    #     pass

    # def test_check_snapshots_helium_wtf_error(self):
    #     pass

    # def test_check_snapshot_download_or_loading_failed_error(self):
    #     pass

    # def test_check_no_plausible_blocks_in_batch_error(self):
    #     pass

    # def test_check_rpc_to_miner_failed_error(self):
    #     pass

    def test_is_not_synced(self):
        d = BobcatDiagnoser()
        d._logger = MagicMock()
        d.status = "Syncing"
        d.gap = 10000
        self.assertTrue(d.is_not_synced())
        d.gap = 400
        self.assertTrue(d.is_not_synced())

    def test_is_synced(self):
        d = BobcatDiagnoser()
        d._logger = MagicMock()
        d.status = "Syncing"
        d.gap = 300
        self.assertFalse(d.is_not_synced())
        d.gap = 10
        self.assertFalse(d.is_not_synced())
        d.status = "Synced"
        d.gap = -10
        self.assertFalse(d.is_not_synced())

    def test_is_relayed(self):
        d = BobcatDiagnoser()
        d._logger = MagicMock()
        d.public_ip = "33.117.96.28"
        d.p2p_status = "\n".join(
            [
                "+---------+---------+",
                "|  name   |result   |",
                "+---------+---------+",
                "|connected|  yes    |",
                "|dialable |  yes    |",
                "|nat_type |symmetric|",
                "| height  |1148539  |",
                "+---------+---------+",
            ]
        )
        d.peerbook = "\n".join(
            [
                "+---------------------------------------------+",
                "|listen_addrs (prioritized)                   |",
                "+---------------------------------------------+",
                "|/p2p//p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|",
                "+---------------------------------------------+",
            ]
        )
        self.assertTrue(d.is_relayed())

    def test_is_not_relayed(self):
        d = BobcatDiagnoser()
        d._logger = MagicMock()
        d.public_ip = "33.117.96.28"
        d.p2p_status = "\n".join(
            [
                "+---------+-------+",
                "|  name   |result |",
                "+---------+-------+",
                "|connected|  yes  |",
                "|dialable |  yes  |",
                "|nat_type | none  |",
                "| height  |1148539|",
                "+---------+-------+",
            ]
        )
        d.peerbook = "\n".join(
            [
                "+---------------------------+",
                "|listen_addrs (prioritized) |",
                "+---------------------------+",
                "|/ip4/33.117.96.28/tcp/44158|",
                "+---------------------------+",
            ]
        )
        self.assertFalse(d.is_relayed())

    def test_is_network_speed_slow(self):
        mock_logger = MagicMock()
        d = BobcatDiagnoser()
        d._logger = mock_logger
        d.download_speed = "5 Mbit/s"
        d.upload_speed = "3 Mbit/s"
        d.latency = "130.669083ms"
        self.assertTrue(d.is_network_speed_slow())
        mock_logger.assert_has_calls(
            [
                call.warning("Network Status: Download Slow (5 Mbit/s)"),
                call.warning("Network Status: Upload Slow (3 Mbit/s)"),
                call.warning("Network Status: Latency High (130.669083ms)"),
            ],
            any_order=False,
        )

    def test_is_network_speed_fast(self):
        mock_logger = MagicMock()
        d = BobcatDiagnoser()
        d._logger = mock_logger
        d.download_speed = "94 Mbit/s"
        d.upload_speed = "57 Mbit/s"
        d.latency = "7.669083ms"
        self.assertFalse(d.is_network_speed_slow())
        mock_logger.assert_has_calls([call.info("Network Status: Good 📶")], any_order=True)

    def test_is_temperature_cold(self):
        mock_logger = MagicMock()
        d = BobcatDiagnoser()
        d._logger = mock_logger
        d.coldest_temp = -5
        d.hottest_temp = -4
        self.assertTrue(d.is_temperature_dangerous())
        mock_logger.assert_has_calls([call.error("Temperature Status: Cold (-5°C) ❄️")])

    def test_is_temperature_good(self):
        mock_logger = MagicMock()
        d = BobcatDiagnoser()
        d._logger = mock_logger
        d.coldest_temp = 30
        d.hottest_temp = 32
        self.assertFalse(d.is_temperature_dangerous())
        mock_logger.assert_has_calls([call.info("Temperature Status: Good (32°C) ☀️")])

    def test_is_temperature_warm(self):
        mock_logger = MagicMock()
        d = BobcatDiagnoser()
        d._logger = mock_logger
        d.coldest_temp = 67
        d.hottest_temp = 68
        self.assertTrue(d.is_temperature_dangerous())
        mock_logger.assert_has_calls([call.warning("Temperature Status: Warm (68°C) 🔥")])

    def test_is_temperature_hot(self):
        mock_logger = MagicMock()
        d = BobcatDiagnoser()
        d._logger = mock_logger
        d.coldest_temp = 79
        d.hottest_temp = 80
        self.assertTrue(d.is_temperature_dangerous())
        mock_logger.assert_has_calls([call.error("Temperature Status: Hot (80°C) 🌋")])

    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"ota_version": "1.0.2.76"}')
    @patch("json.dump")
    def test_ota_version_changed(
        self, mock_json_dump, mock_open, mock_os_path_isfile, mock_os_path_exists
    ):
        mock_logger = MagicMock()
        d = BobcatDiagnoser()
        d._logger = mock_logger
        d._state_file = "/etc/bobcat/autopilot.json"
        d.ota_version = "1.0.2.77"
        self.assertTrue(d.did_ota_version_change())
        mock_logger.assert_has_calls([call.warning(f"New OTA Version: {d.ota_version}")])
        mock_json_dump.called_once_with({"ota_version": "1.0.2.77"}, mock_open)

    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"ota_version": "1.0.2.77"}')
    @patch("json.dump")
    def test_ota_version_not_changed(
        self, mock_json_dump, mock_open, mock_os_path_isfile, mock_os_path_exists
    ):
        mock_logger = MagicMock()
        d = BobcatDiagnoser()
        d._logger = mock_logger
        d._state_file = "/etc/bobcat/autopilot.json"
        d.ota_version = "1.0.2.77"
        self.assertFalse(d.did_ota_version_change())
        self.assertFalse(mock_logger.called)
        mock_json_dump.called_once_with({"ota_version": "1.0.2.77"}, mock_open)


if __name__ == "__main__":
    unittest.main()
