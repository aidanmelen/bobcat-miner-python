from unittest.mock import PropertyMock, AsyncMock, MagicMock, patch, call, mock_open

import unittest

from bobcat_miner import (
    Bobcat,
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
    UnknownErrorCheck,
    OnlineStatusCheck,
    RelayStatusCheck,
    SyncStatusCheck,
    NetworkStatusCheck,
    TemperatureStatusCheck,
    OTAVersionStatusCheck,
)

import mock_endpoints


class TestDownOrErrorCheck(unittest.TestCase):
    def setUp(self):
        self.mock_bobcat = MagicMock(spec=Bobcat)
        self.mock_bobcat.logger = MagicMock()
        mock_verbose = False
        self.check = DownOrErrorCheck(self.mock_bobcat, mock_verbose)

    def test_DownOrErrorCheck_when_error(self):
        self.mock_bobcat.status = "Error"
        self.mock_bobcat.tip = " Error response from daemon: Container 49dd5fae6f3094e240e9aa339947bc9f6336d5f997c495a37696095fc306f3d1 is restarting, wait until the container is running exit status 1"

        self.assertTrue(self.check.check())

        self.check.verbose = True
        self.assertTrue(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.error("Bobcat Status: Error", extra={}),
                call.error("Bobcat Status: Error", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    def test_DownOrErrorCheck_when_down(self):
        self.mock_bobcat.status = "Down"
        self.assertTrue(self.check.check())

        self.check.verbose = True
        self.assertTrue(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.error("Bobcat Status: Down", extra={}),
                call.error("Bobcat Status: Down", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    def test_DownOrErrorCheck_when_synced(self):
        self.mock_bobcat.status = "Synced"
        self.mock_bobcat.tip = ""
        self.assertFalse(self.check.check())
        self.assertFalse(self.mock_bobcat.logger.called)


class TestHeightAPIErrorCheck(unittest.TestCase):
    def setUp(self):
        self.mock_bobcat = MagicMock(spec=Bobcat)
        self.mock_bobcat.logger = MagicMock()
        mock_verbose = False
        self.check = HeightAPIErrorCheck(self.mock_bobcat, mock_verbose)

    def test_HeightAPIErrorCheck_when_error(self):
        self.mock_bobcat.status = "Height API Error"

        self.assertTrue(self.check.check())

        self.check.verbose = True
        self.assertTrue(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.error("Bobcat Status: Height API Error", extra={}),
                call.error(
                    "Bobcat Status: Height API Error", extra={"description": str(self.check)}
                ),
            ],
            any_order=False,
        )

    def test_HeightAPIErrorCheck_when_synced(self):
        self.mock_bobcat.status = "Synced"
        self.assertFalse(self.check.check())
        self.assertFalse(self.mock_bobcat.logger.called)


class TestUnknownErrorCheck(unittest.TestCase):
    def setUp(self):
        self.mock_bobcat = MagicMock(spec=Bobcat)
        self.mock_bobcat.logger = MagicMock()
        mock_verbose = False
        self.check = UnknownErrorCheck(self.mock_bobcat, mock_verbose)

    def test_UnknownErrorCheck_when_error(self):

        # Please see observations docs for more information about test setup:
        # https://github.com/aidanmelen/bobcat-miner-python/tree/main/docs/observations/errors/unknown-error.md
        self.mock_bobcat.is_healthy = False
        self.mock_bobcat.status = "Unkown"
        self.mock_bobcat.gap = "-"
        self.mock_bobcat.region = ("error: usage in",)
        self.mock_bobcat.p2p_status = [
            "Error: Usage information not found for the given command",
            "",
            "",
            "",
        ]
        self.epoch = "Error:"
        self.mock_bobcat.height = [
            "Error: Usage information not found for the given command",
            "",
            "",
            "",
        ]
        self.miner_alert = None
        self.error = ""

        self.assertTrue(self.check.check())

        self.check.verbose = True
        self.assertTrue(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.error("Bobcat Status: Unkown", extra={}),
                call.error("Bobcat Status: Unkown", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )


class TestOnlineStatusCheck(unittest.TestCase):
    def setUp(self):
        self.mock_bobcat = MagicMock(spec=Bobcat)
        self.mock_bobcat.logger = MagicMock()
        self.mock_bobcat._trace = False
        mock_verbose = False
        self.check = OnlineStatusCheck(self.mock_bobcat, mock_verbose)

    @patch("requests.get", side_effect=mock_endpoints.mock_online)
    def test_OnlineStatusCheck_when_online(self, mock_requests_get):
        self.mock_bobcat.is_healthy = True
        self.mock_bobcat.miner_state = "running"
        self.assertFalse(self.check.check())

    @patch("requests.get", side_effect=mock_endpoints.mock_offline)
    def test_OnlineStatusCheck_when_offline(self, mock_requests_get):
        self.mock_bobcat.is_healthy = False
        self.assertTrue(self.check.check())

    @patch("requests.get", side_effect=mock_endpoints.mock_healthy_and_helium_api_is_stale)
    def test_OnlineStatusCheck_when_healthy_but_helium_api_is_stale(self, mock_requests_get):
        self.mock_bobcat.is_healthy = True
        self.mock_bobcat.miner_state = "running"
        self.assertFalse(self.check.check())

    @patch("requests.get", side_effect=Exception("Unable to Reach Helium API"))
    def test_OnlineStatusCheck_when_helium_api_is_unreachable_and_not_running(
        self, mock_requests_get
    ):
        self.assertFalse(self.check.check())


class TestSyncStatusCheck(unittest.TestCase):
    def setUp(self):
        self.mock_bobcat = MagicMock(spec=Bobcat)
        self.mock_bobcat.logger = MagicMock()
        self.mock_bobcat.status = "Syncing"
        mock_verbose = False
        self.check = SyncStatusCheck(self.mock_bobcat, mock_verbose)

    def test_SyncStatusCheck_when_not_synced(self):
        self.mock_bobcat.gap = 10000
        self.assertTrue(self.check.check())

        self.mock_bobcat.gap = 400
        self.assertTrue(self.check.check())

        self.check.verbose = True
        self.assertTrue(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.error("Sync Status: Syncing (gap:10000)", extra={}),
                call.error("Sync Status: Syncing (gap:400)", extra={}),
                call.error(
                    "Sync Status: Syncing (gap:400)", extra={"description": str(self.check)}
                ),
            ],
            any_order=False,
        )

    def test_SyncStatusCheck_when_synced(self):
        self.mock_bobcat.gap = 300
        self.assertFalse(self.check.check())

        self.mock_bobcat.gap = 10
        self.assertFalse(self.check.check())

        self.mock_bobcat.status = "Synced"
        self.mock_bobcat.gap = -10
        self.assertFalse(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.info("Sync Status: Syncing (gap:300) 💫"),
                call.info("Sync Status: Syncing (gap:10) 💫"),
                call.info("Sync Status: Synced (gap:-10) 💫"),
            ],
            any_order=False,
        )


class TestRelayStatusCheck(unittest.TestCase):
    def setUp(self):
        self.mock_bobcat = MagicMock(spec=Bobcat)
        self.mock_bobcat.logger = MagicMock()
        self.mock_bobcat.public_ip = "33.117.96.28"
        mock_verbose = False
        self.check = RelayStatusCheck(self.mock_bobcat, mock_verbose)

    def test_RelayStatusCheck_when_not_relayed(self):
        self.mock_bobcat.p2p_status = "\n".join(
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
        self.mock_bobcat.peerbook = "\n".join(
            [
                "+---------------------------------------------+",
                "|listen_addrs (prioritized)                   |",
                "+---------------------------------------------+",
                "|/p2p//p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|",
                "+---------------------------------------------+",
            ]
        )

        self.assertFalse(self.check.check())

        self.check.verbose = True
        self.assertFalse(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.error("Relay Status: Relayed"),
                call.error("Relay Status: Relayed", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    def test_RelayStatusCheck_when_not_relayed(self):
        self.mock_bobcat.p2p_status = "\n".join(
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
        self.mock_bobcat.peerbook = "\n".join(
            [
                "+---------------------------+",
                "|listen_addrs (prioritized) |",
                "+---------------------------+",
                "|/ip4/33.117.96.28/tcp/44158|",
                "+---------------------------+",
            ]
        )
        self.assertFalse(self.check.check())
        self.mock_bobcat.logger.info.assert_called_once_with("Relay Status: Not Relayed ✨")


class TestNetworkStatusCheck(unittest.TestCase):
    def setUp(self):
        self.mock_bobcat = MagicMock(spec=Bobcat)
        self.mock_bobcat.logger = MagicMock()
        mock_verbose = False
        self.check = NetworkStatusCheck(self.mock_bobcat, mock_verbose)

    def test_NetworkStatusCheck_when_slow(self):
        self.mock_bobcat.download_speed = "5 Mbit/s"
        self.mock_bobcat.upload_speed = "3 Mbit/s"
        self.mock_bobcat.latency = "130.669083ms"
        self.assertTrue(self.check.check())

        self.check.verbose = True
        self.mock_bobcat.download_speed = "5 Mbit/s"
        self.mock_bobcat.upload_speed = "3 Mbit/s"
        self.mock_bobcat.latency = "130.669083ms"
        self.assertTrue(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.warning("Network Status: Download Slow (5 Mbit/s)", extra={}),
                call.warning("Network Status: Upload Slow (3 Mbit/s)", extra={}),
                call.warning("Network Status: Latency High (130.669083ms)", extra={}),
                call.warning(
                    "Network Status: Download Slow (5 Mbit/s)",
                    extra={"description": str(self.check)},
                ),
                call.warning(
                    "Network Status: Upload Slow (3 Mbit/s)", extra={"description": str(self.check)}
                ),
                call.warning(
                    "Network Status: Latency High (130.669083ms)",
                    extra={"description": str(self.check)},
                ),
            ],
            any_order=False,
        )

    def test_NetworkStatusCheck_when_good(self):
        self.mock_bobcat.download_speed = "94 Mbit/s"
        self.mock_bobcat.upload_speed = "57 Mbit/s"
        self.mock_bobcat.latency = "7.669083ms"
        self.assertFalse(self.check.check())
        self.mock_bobcat.logger.info.assert_called_once_with("Network Status: Good 📶")


class TestTemperatureStatusCheck(unittest.TestCase):
    def setUp(self):
        self.mock_bobcat = MagicMock(spec=Bobcat)
        self.mock_bobcat.logger = MagicMock()
        mock_verbose = False
        self.check = TemperatureStatusCheck(self.mock_bobcat, mock_verbose)

    def test_TemperatureStatusCheck_when_cold(self):
        self.mock_bobcat.coldest_temp = -5
        self.mock_bobcat.hottest_temp = -4

        self.assertTrue(self.check.check())

        self.check.verbose = True
        self.assertTrue(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.error("Temperature Status: Cold (-5°C) ❄️", extra={}),
                call.error(
                    "Temperature Status: Cold (-5°C) ❄️", extra={"description": str(self.check)}
                ),
            ],
            any_order=False,
        )

    def test_TemperatureStatusCheck_when_good(self):
        self.mock_bobcat.coldest_temp = 30
        self.mock_bobcat.hottest_temp = 32
        self.assertFalse(self.check.check())
        self.mock_bobcat.logger.info.assert_called_once_with("Temperature Status: Good (32°C) ☀️")

    def test_TemperatureStatusCheck_when_warm(self):
        self.mock_bobcat.coldest_temp = 67
        self.mock_bobcat.hottest_temp = 68

        self.assertTrue(self.check.check())

        self.check.verbose = True
        self.assertTrue(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.warning("Temperature Status: Warm (68°C) 🔥", extra={}),
                call.warning(
                    "Temperature Status: Warm (68°C) 🔥", extra={"description": str(self.check)}
                ),
            ],
            any_order=False,
        )

    def test_TemperatureStatusCheck_when_hot(self):
        self.mock_bobcat.coldest_temp = 79
        self.mock_bobcat.hottest_temp = 80
        self.assertTrue(self.check.check())

        self.assertTrue(self.check.check())

        self.check.verbose = True
        self.assertTrue(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.error("Temperature Status: Hot (80°C) 🌋", extra={}),
                call.error(
                    "Temperature Status: Hot (80°C) 🌋", extra={"description": str(self.check)}
                ),
            ],
            any_order=False,
        )


class TestOTAVersionStatusCheck(unittest.TestCase):
    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=True)
    def setUp(self, mock_os_path_isfile, mock_os_path_exists):
        self.mock_bobcat = MagicMock(spec=Bobcat)
        self.mock_bobcat.logger = MagicMock()
        self.mock_bobcat.ota_version = "1.0.2.77"
        mock_verbose = False
        mock_state_file = "/etc/bobcat/autopilot.json"
        self.check = OTAVersionStatusCheck(self.mock_bobcat, mock_verbose, mock_state_file)

    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open, read_data='{"ota_version": "1.0.2.76"}')
    def test_OTAVersionStatusCheck_when_version_changed(self, mock_open, mock_json_dump):
        self.assertTrue(self.check.check())
        mock_json_dump.called_once_with({"ota_version": "1.0.2.77"}, mock_open)

        self.check.verbose = True
        self.assertTrue(self.check.check())

        self.check.bobcat.logger.assert_has_calls(
            [
                call.warning("New OTA Version: 1.0.2.77", extra={}),
                call.warning("New OTA Version: 1.0.2.77", extra={"description": str(self.check)}),
            ],
            any_order=False,
        )

    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open, read_data='{"ota_version": "1.0.2.77"}')
    def test_OTAVersionStatusCheck_when_version_not_changed(self, mock_open, mock_json_dump):
        mocklogger = MagicMock()
        self.assertFalse(self.check.check())
        self.assertFalse(self.mock_bobcat.logger.called)
        mock_json_dump.called_once_with({"ota_version": "1.0.2.77"}, mock_open)


if __name__ == "__main__":
    unittest.main()
