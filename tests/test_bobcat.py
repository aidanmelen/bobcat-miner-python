from unittest.mock import call, patch, AsyncMock, PropertyMock, MagicMock

import unittest

from bobcat_miner import Bobcat, BobcatConnectionError

import mock_endpoints


DISABLED = 100


class TestBobcat(unittest.TestCase):
    """Test Bobcat."""

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.get", side_effect=mock_endpoints.mock_online)
    def setUp(self, mock_requests_get, mock_bobcat_conn_is_bobcat):
        self.mock_hostname = "192.168.0.10"
        self.mock_animal = "fancy-awesome-bobcat"
        self.bobcat = Bobcat(hostname=self.mock_hostname, log_level=DISABLED)
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
        self.assertEqual(self.bobcat.ota_version, "1.0.2.76")

    def test_region(self):
        self.assertEqual(self.bobcat.region, "region_us915")

    def test_frequency_plan(self):
        self.assertEqual(self.bobcat.frequency_plan, "us915")

    def test_animal(self):
        self.assertEqual(self.bobcat.animal, "fancy-awesome-bobcat")

    def test_helium_animal(self):
        self.assertEqual(self.bobcat.helium_animal, "Fancy Awesome Bobcat")

    def test_pubkey(self):
        self.assertEqual(
            self.bobcat.pubkey,
            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        )

    def test_miner_state(self):
        self.assertEqual(self.bobcat.miner_state, "running")

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

    def test_is_healthy(self):
        self.assertTrue(self.bobcat.is_healthy)

    @patch("bobcat_miner.Bobcat.heartbeat")
    @patch("bobcat_miner.Bobcat.wait")
    @patch("requests.post", side_effect=mock_endpoints.mock_online)
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_reboot(self, mock_verify, mock_requests_post, mock_wait, mock_heartbeat):
        Bobcat(hostname=self.mock_hostname, log_level=DISABLED).reboot()
        mock_requests_post.assert_called_once_with(
            f"http://{self.mock_hostname}/admin/reboot",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("bobcat_miner.Bobcat.heartbeat")
    @patch("bobcat_miner.Bobcat.wait")
    @patch("requests.post", side_effect=mock_endpoints.mock_online)
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_reset(self, mock_verify, mock_requests_post, mock_wait, mock_heartbeat):
        Bobcat(hostname=self.mock_hostname, log_level=DISABLED).reset()
        mock_requests_post.assert_called_once_with(
            f"http://{self.mock_hostname}/admin/reset",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("bobcat_miner.Bobcat.heartbeat")
    @patch("bobcat_miner.Bobcat.wait")
    @patch("requests.post", side_effect=mock_endpoints.mock_online)
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_resync(self, mock_verify, mock_requests_post, mock_wait, mock_heartbeat):
        Bobcat(hostname=self.mock_hostname, log_level=DISABLED).resync()
        mock_requests_post.assert_called_once_with(
            f"http://{self.mock_hostname}/admin/resync",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )

    @patch("bobcat_miner.Bobcat.heartbeat")
    @patch("bobcat_miner.Bobcat.wait")
    @patch("requests.post", side_effect=mock_endpoints.mock_online)
    @patch("requests.get", side_effect=mock_endpoints.mock_online)
    @patch("bobcat_miner.Bobcat.is_healthy", new_callable=PropertyMock, return_value=True)
    @patch("bobcat_miner.Bobcat.gap", new_callable=PropertyMock, return_value=1000)
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_fastsync(
        self,
        mock_verify,
        mock_gap,
        mock_is_healthy,
        mock_requests_get,
        mock_requests_post,
        mock_wait,
        mock_heartbeat,
    ):
        b = Bobcat(hostname=self.mock_hostname)
        b.logger = MagicMock()
        b.fastsync()
        mock_requests_post.assert_called_once_with(
            f"http://{self.mock_hostname}/admin/fastsync",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )
        b.logger.debug.assert_has_calls(
            [call("Refresh: Status Data"), call("Syncing your miner, please leave your power on.")]
        )

    @patch("bobcat_miner.Bobcat.heartbeat")
    @patch("bobcat_miner.Bobcat.wait")
    @patch("requests.post", side_effect=mock_endpoints.mock_online)
    @patch("requests.get", side_effect=mock_endpoints.mock_online)
    @patch("bobcat_miner.Bobcat.gap", new_callable=PropertyMock, return_value="mock bad gap")
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_fastsync_should_skip_when_unable_to_read_gap(
        self,
        mock_verify,
        mock_gap,
        mock_requests_get,
        mock_requests_post,
        mock_wait,
        mock_heartbeat,
    ):
        b = Bobcat(hostname=self.mock_hostname)
        b.logger = MagicMock()
        b.fastsync()
        b.logger.debug.assert_called_once_with("Refresh: Status Data")
        b.logger.error.assert_called_once_with(
            "Cancelling the Fastsync. Unable to read the blockchain gap (mock bad gap)"
        )
        self.assertFalse(mock_requests_post.called)

    @patch("bobcat_miner.Bobcat.heartbeat")
    @patch("bobcat_miner.Bobcat.wait")
    @patch("requests.post", side_effect=mock_endpoints.mock_online)
    @patch("requests.get", side_effect=mock_endpoints.mock_online)
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_fastsync_should_skip_when_gap_is_less_than_400(
        self,
        mock_verify,
        mock_requests_get,
        mock_requests_post,
        mock_wait,
        mock_heartbeat,
    ):
        b = Bobcat(hostname=self.mock_hostname)
        b.logger = MagicMock()
        b.fastsync()
        b.logger.debug.assert_called_once_with("Refresh: Status Data")
        b.logger.warning.assert_called_once_with(
            "Cancelling Fastsync because it only works when the gap is larger than 400. The current gap is: 0"
        )
        self.assertFalse(mock_requests_post.called)

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("time.sleep")
    def test_wait(self, mock_sleep, mock_verify):
        b = Bobcat(hostname=self.mock_hostname)
        b.logger = MagicMock()
        b.wait(duration=300)
        b.logger.debug.assert_called_once_with("Waiting for 5 Minutes ⏳")
        mock_sleep.assert_called_once_with(300)

    @patch("bobcat_miner.Bobcat.animal", new_callable=PropertyMock)
    @patch("bobcat_miner.Bobcat.wait")
    @patch("bobcat_miner.BobcatConnection.can_connect", side_effect=[False, False, True])
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_wait_for_connection(self, mock_verify, mock_can_connect, mock_wait, mock_animal):
        mock_animal.return_value = self.mock_animal

        b = Bobcat(hostname=self.mock_hostname)
        b.logger = MagicMock()
        b.wait_for_connection(backoff_duration=300, max_attempts=3)

        mock_wait.assert_has_calls([call(300), call(300)])
        b.logger.warning.assert_has_calls(
            [
                call(f"The Bobcat ({self.mock_animal}) is unreachable"),
                call(f"The Bobcat ({self.mock_animal}) is unreachable"),
            ]
        )

    @patch("bobcat_miner.Bobcat.animal", new_callable=PropertyMock)
    @patch("bobcat_miner.Bobcat.wait")
    @patch("bobcat_miner.BobcatConnection.can_connect", side_effect=[False, False, False, False])
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_wait_for_connection_throw_connection_error_after_max_tries(
        self, mock_verify, mock_can_connect, mock_wait, mock_animal
    ):
        mock_animal.return_value = self.mock_animal

        b = Bobcat(hostname=self.mock_hostname)
        b.logger = MagicMock()

        with self.assertRaises(BobcatConnectionError) as err:
            b.wait_for_connection(backoff_duration=300, max_attempts=3)

        mock_wait.assert_called_with(300)
        self.assertEqual(mock_wait.call_count, 3)

        b.logger.warning.assert_called_with(f"The Bobcat ({self.mock_animal}) is unreachable")
        self.assertEqual(b.logger.warning.call_count, 3)

    @patch("bobcat_miner.Bobcat.wait")
    @patch("bobcat_miner.Bobcat.animal", new_callable=PropertyMock)
    @patch("bobcat_miner.Bobcat.miner_state", new_callable=PropertyMock)
    @patch("bobcat_miner.BobcatAPI.refresh")
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_wait_until_running(
        self, mock_verify, mock_refresh, mock_miner_state, mock_animal, mock_wait
    ):
        mock_miner_state.side_effect = ["None", "", "", "running"]
        mock_animal.return_value = self.mock_animal

        b = Bobcat(hostname=self.mock_hostname)
        b.logger = MagicMock()
        b.wait_until_running(backoff_duration=300, max_attempts=12)

        mock_wait.assert_has_calls([call(300), call(300), call(300)], any_order=False)

        b.logger.warning.assert_has_calls(
            [
                call("The Bobcat (fancy-awesome-bobcat) is not running"),
                call("The Bobcat (fancy-awesome-bobcat) is not running"),
                call("The Bobcat (fancy-awesome-bobcat) is not running"),
            ],
            any_order=False,
        )

    @patch("bobcat_miner.Bobcat.wait")
    @patch("bobcat_miner.Bobcat.animal", new_callable=PropertyMock)
    @patch("bobcat_miner.Bobcat.miner_state", new_callable=PropertyMock)
    @patch("bobcat_miner.BobcatAPI.refresh")
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_wait_until_running_logs_warning_after_max_tries(
        self, mock_verify, mock_refresh, mock_miner_state, mock_animal, mock_wait
    ):
        mock_miner_state.side_effect = ["None", "", "", ""]
        mock_animal.return_value = self.mock_animal

        b = Bobcat(hostname=self.mock_hostname)
        b.logger = MagicMock()
        b.wait_until_running(backoff_duration=300, max_attempts=2)

        mock_wait.assert_called_with(300)
        self.assertEqual(mock_wait.call_count, 2)

        b.logger.warning.assert_has_calls(
            [
                call("The Bobcat (fancy-awesome-bobcat) is not running"),
                call("The Bobcat (fancy-awesome-bobcat) is not running"),
                call("Waited for 10 minutes and still not running"),
            ],
            any_order=False,
        )

    @patch("bobcat_miner.Bobcat.animal", new_callable=PropertyMock)
    @patch("bobcat_miner.Bobcat.wait_for_connection")
    @patch("bobcat_miner.Bobcat.wait_until_running")
    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_heartbeat(
        self, mock_verify, mock_wait_for_connection, mock_wait_until_running, mock_animal
    ):
        mock_animal.return_value = self.mock_animal

        b = Bobcat(hostname=self.mock_hostname)
        b.logger = MagicMock()
        b.heartbeat(backoff_duration=300, max_attempts=3)

        mock_wait_for_connection.assert_called_once_with(300, 3)
        mock_wait_until_running.assert_called_once_with(300, 3)
        b.logger.info.assert_called_once_with(f"Reconnected to the Bobcat ({self.mock_animal})")


if __name__ == "__main__":
    unittest.main()
