from unittest.mock import MagicMock, patch, call, mock_open

import unittest

from bobcat_miner import (
    OnlineStatusCheck,
    RelayStatusCheck,
    SyncStatusCheck,
    NetworkStatusCheck,
    TemperatureStatusCheck,
    OTAVersionStatusCheck,
    DownOrErrorCheck,
    HeightAPIErrorCheck,
    # NoActivityCheck,
    # NoWitnessesCheck,
    # BlockChecksumMismatchErrorCheck,
    # CompressionMethodorCorruptedErrorCheck,
    # TooManyLookupAttemptsErrorCheck,
    # OnboardingDewiOrgNxdomainErrorCheck,
    # FailedToStartChildErrorCheck,
    # NotADetsFileErrorCheck,
    # SnapshotsHeliumWTFErrorCheck,
    # SnapshotDownloadOrLoadingFailedErrorCheck,
    # NoPlausibleBlocksInBatchErrorCheck,
    # RPCFailedCheck,
)


class TestRelayStatusCheck(unittest.TestCase):
    def setUp(self):
        self.mock_autopilot = MagicMock()
        self.mock_autopilot._logger = MagicMock()
        self.mock_autopilot.public_ip = "33.117.96.28"
        self.check = RelayStatusCheck(self.mock_autopilot)

    def test_RelayStatusCheck_when_not_relayed(self):
        self.mock_autopilot.p2p_status = "\n".join(
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
        self.mock_autopilot.peerbook = "\n".join(
            [
                "+---------------------------------------------+",
                "|listen_addrs (prioritized)                   |",
                "+---------------------------------------------+",
                "|/p2p//p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|",
                "+---------------------------------------------+",
            ]
        )

        self.mock_autopilot._verbose = False
        self.assertFalse(self.check.check())

        self.mock_autopilot._verbose = True
        self.assertFalse(self.check.check())

        self.mock_autopilot._logger.assert_has_calls(
            [
                call.error("Relay Status: Relayed"),
                call.error("Relay Status: Relayed", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    def test_RelayStatusCheck_when_not_relayed(self):
        self.mock_autopilot.p2p_status = "\n".join(
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
        self.mock_autopilot.peerbook = "\n".join(
            [
                "+---------------------------+",
                "|listen_addrs (prioritized) |",
                "+---------------------------+",
                "|/ip4/33.117.96.28/tcp/44158|",
                "+---------------------------+",
            ]
        )
        self.assertFalse(self.check.check())
        self.mock_autopilot._logger.info.assert_called_once_with("Relay Status: Not Relayed ✨")


class TestSyncStatusCheck(unittest.TestCase):
    def setUp(self):
        self.mock_autopilot = MagicMock()
        self.mock_autopilot._verbose = False
        self.mock_autopilot._logger = MagicMock()
        self.mock_autopilot.status = "Syncing"
        self.check = SyncStatusCheck(self.mock_autopilot)

    def test_SyncStatusCheck_when_not_synced(self):
        self.mock_autopilot.gap = 10000
        self.assertTrue(self.check.check())

        self.mock_autopilot.gap = 400
        self.assertTrue(self.check.check())

        self.mock_autopilot._verbose = True
        self.assertTrue(self.check.check())

        self.mock_autopilot._logger.assert_has_calls(
            [
                call.error("Sync Status: Syncing (gap:10000)", extra={}),
                call.error("Sync Status: Syncing (gap:400)", extra={}),
                call.error("Sync Status: Syncing (gap:400)", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    def test_SyncStatusCheck_when_synced(self):
        self.mock_autopilot.gap = 300
        self.assertFalse(self.check.check())

        self.mock_autopilot.gap = 10
        self.assertFalse(self.check.check())

        self.mock_autopilot.status = "Synced"
        self.mock_autopilot.gap = -10
        self.assertFalse(self.check.check())

        self.mock_autopilot._logger.assert_has_calls(
            [
                call.info("Sync Status: Syncing (gap:300) ✨"),
                call.info("Sync Status: Syncing (gap:10) ✨"),
                call.info("Sync Status: Synced (gap:-10) ✨"),
            ],
            any_order=False,
        )


class TestNetworkStatusCheck(unittest.TestCase):
    def setUp(self):
        self.mock_autopilot = MagicMock()
        self.mock_autopilot._logger = MagicMock()
        self.check = NetworkStatusCheck(self.mock_autopilot)

    def test_NetworkStatusCheck_when_slow(self):
        self.mock_autopilot._verbose = False
        self.mock_autopilot.download_speed = "5 Mbit/s"
        self.mock_autopilot.upload_speed = "3 Mbit/s"
        self.mock_autopilot.latency = "130.669083ms"
        self.assertTrue(self.check.check())

        self.mock_autopilot._verbose = True
        self.mock_autopilot.download_speed = "5 Mbit/s"
        self.mock_autopilot.upload_speed = "3 Mbit/s"
        self.mock_autopilot.latency = "130.669083ms"
        self.assertTrue(self.check.check())

        self.mock_autopilot._logger.assert_has_calls(
            [
                call.warning("Network Status: Download Slow (5 Mbit/s)", extra={}),
                call.warning("Network Status: Upload Slow (3 Mbit/s)", extra={}),
                call.warning("Network Status: Latency High (130.669083ms)", extra={}),
                call.warning("Network Status: Download Slow (5 Mbit/s)", extra={"description": str(self.check)}),
                call.warning("Network Status: Upload Slow (3 Mbit/s)", extra={"description": str(self.check)}),
                call.warning("Network Status: Latency High (130.669083ms)", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    def test_NetworkStatusCheck_when_good(self):
        self.mock_autopilot.download_speed = "94 Mbit/s"
        self.mock_autopilot.upload_speed = "57 Mbit/s"
        self.mock_autopilot.latency = "7.669083ms"
        self.assertFalse(self.check.check())
        self.mock_autopilot._logger.info.assert_called_once_with("Network Status: Good 📶")


class TestTemperatureStatusCheck(unittest.TestCase):
    def setUp(self):
        self.mock_autopilot = MagicMock()
        self.mock_autopilot._logger = MagicMock()
        self.check = TemperatureStatusCheck(self.mock_autopilot)

    def test_TemperatureStatusCheck_when_cold(self):
        self.mock_autopilot.coldest_temp = -5
        self.mock_autopilot.hottest_temp = -4

        self.mock_autopilot._verbose = False
        self.assertTrue(self.check.check())

        self.mock_autopilot._verbose = True
        self.assertTrue(self.check.check())

        self.mock_autopilot._logger.assert_has_calls(
            [
                call.error("Temperature Status: Cold (-5°C) ❄️", extra={}),
                call.error("Temperature Status: Cold (-5°C) ❄️", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    def test_TemperatureStatusCheck_when_good(self):
        self.mock_autopilot.coldest_temp = 30
        self.mock_autopilot.hottest_temp = 32
        self.assertFalse(self.check.check())
        self.mock_autopilot._logger.info.assert_called_once_with(
            "Temperature Status: Good (32°C) ☀️"
        )

    def test_TemperatureStatusCheck_when_warm(self):
        self.mock_autopilot.coldest_temp = 67
        self.mock_autopilot.hottest_temp = 68

        self.mock_autopilot._verbose = False
        self.assertTrue(self.check.check())

        self.mock_autopilot._verbose = True
        self.assertTrue(self.check.check())

        self.mock_autopilot._logger.assert_has_calls(
            [
                call.warning("Temperature Status: Warm (68°C) 🔥", extra={}),
                call.warning("Temperature Status: Warm (68°C) 🔥", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    def test_TemperatureStatusCheck_when_hot(self):
        self.mock_autopilot.coldest_temp = 79
        self.mock_autopilot.hottest_temp = 80
        self.assertTrue(self.check.check())

        self.mock_autopilot._verbose = False
        self.assertTrue(self.check.check())

        self.mock_autopilot._verbose = True
        self.assertTrue(self.check.check())

        self.mock_autopilot._logger.assert_has_calls(
            [
                call.error("Temperature Status: Hot (80°C) 🌋", extra={}),
                call.error("Temperature Status: Hot (80°C) 🌋", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )


class TestOTAVersionStatusCheck(unittest.TestCase):
    def setUp(self):
        self.mock_autopilot = MagicMock()
        self.mock_autopilot._logger = MagicMock()
        self.mock_autopilot._state_file = "/etc/bobcat/autopilot.json"
        self.mock_autopilot.ota_version = "1.0.2.77"
        self.check = OTAVersionStatusCheck(self.mock_autopilot)

    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"ota_version": "1.0.2.76"}')
    @patch("json.dump")
    def test_OTAVersionStatusCheck_when_version_changed(
        self, mock_json_dump, mock_open, mock_os_path_isfile, mock_os_path_exists
    ):
        self.mock_autopilot._verbose = False
        self.assertTrue(self.check.check())
        mock_json_dump.called_once_with({"ota_version": "1.0.2.77"}, mock_open)

        self.mock_autopilot._verbose = True
        self.assertTrue(self.check.check())

        self.mock_autopilot._logger.assert_has_calls(
            [
                call.warning("New OTA Version: 1.0.2.77", extra={}),
                call.warning("New OTA Version: 1.0.2.77", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )


    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"ota_version": "1.0.2.77"}')
    @patch("json.dump")
    def test_OTAVersionStatusCheck_when_version_not_changed(
        self, mock_json_dump, mock_open, mock_os_path_isfile, mock_os_path_exists
    ):
        mock_logger = MagicMock()
        self.assertFalse(self.check.check())
        self.assertFalse(self.mock_autopilot._logger.called)
        mock_json_dump.called_once_with({"ota_version": "1.0.2.77"}, mock_open)


class TestDownOrErrorCheck(unittest.TestCase):
    def setUp(self):
        self.mock_autopilot = MagicMock()
        self.mock_autopilot._verbose = False
        self.mock_autopilot._logger = MagicMock()
        self.check = DownOrErrorCheck(self.mock_autopilot)

    def test_DownOrErrorCheck_when_error(self):
        self.mock_autopilot.status = "Error"
        self.mock_autopilot.tip = " Error response from daemon: Container 49dd5fae6f3094e240e9aa339947bc9f6336d5f997c495a37696095fc306f3d1 is restarting, wait until the container is running exit status 1"

        self.mock_autopilot._verbose = False
        self.assertTrue(self.check.check())

        self.mock_autopilot._verbose = True
        self.assertTrue(self.check.check())

        self.mock_autopilot._logger.assert_has_calls(
            [
                call.error("Bobcat Status: Error", extra={}),
                call.error("Bobcat Status: Error", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    def test_DownOrErrorCheck_when_down(self):
        self.mock_autopilot.status = "Down"

        self.mock_autopilot._verbose = False
        self.assertTrue(self.check.check())

        self.mock_autopilot._verbose = True
        self.assertTrue(self.check.check())

        self.mock_autopilot._logger.assert_has_calls(
            [
                call.error("Bobcat Status: Down", extra={}),
                call.error("Bobcat Status: Down", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    def test_DownOrErrorCheck_when_synced(self):
        self.mock_autopilot.status = "Synced"
        self.mock_autopilot.tip = ""
        self.assertFalse(self.check.check())
        self.assertFalse(self.mock_autopilot._logger.called)


class TestHeightAPIErrorCheck(unittest.TestCase):
    def setUp(self):
        self.mock_autopilot = MagicMock()
        self.mock_autopilot._logger = MagicMock()
        self.check = HeightAPIErrorCheck(self.mock_autopilot)

    def test_HeightAPIErrorCheck_when_error(self):
        self.mock_autopilot.status = "Height API Error"

        self.mock_autopilot._verbose = False
        self.assertTrue(self.check.check())

        self.mock_autopilot._verbose = True
        self.assertTrue(self.check.check())

        self.mock_autopilot._logger.assert_has_calls(
            [
                call.error("Bobcat Status: Height API Error", extra={}),
                call.error("Bobcat Status: Height API Error", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    def test_HeightAPIErrorCheck_when_synced(self):
        self.mock_autopilot.status = "Synced"
        self.assertFalse(self.check.check())
        self.assertFalse(self.mock_autopilot._logger.called)


if __name__ == "__main__":
    unittest.main()
