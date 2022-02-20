from unittest.mock import patch, AsyncMock
from unittest.mock import call

import unittest

from bobcat_miner import BobcatAPI

import mock_endpoints

DISABLED = 100


class TestBobcatAPI(unittest.TestCase):
    """Test BobcatAPI."""

    def setUp(self):
        self.mock_hostname = "192.168.0.10"

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.get")
    def test_refresh_status(self, mock_requests_get, mock_bobcat_conn_is_bobcat):
        BobcatAPI(hostname=self.mock_hostname, log_level=DISABLED).refresh_status()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/status.json")

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("bobcat_miner.BobcatConnection._BobcatConnection__refresh_miner")
    def test_refresh_miner(self, mock_refresh_miner, mock_verify):
        BobcatAPI(hostname=self.mock_hostname, log_level=DISABLED).refresh_miner()
        mock_refresh_miner.assert_called_once_with()

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.get")
    def test_refresh_temp(self, mock_requests_get, mock_verify):
        BobcatAPI(hostname=self.mock_hostname, log_level=DISABLED).refresh_temp()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/temp.json")

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.get")
    def test_refresh_speed(self, mock_requests_get, mock_verify):
        BobcatAPI(hostname=self.mock_hostname, log_level=DISABLED).refresh_speed()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/speed.json")

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.get")
    def test_refresh_dig(self, mock_requests_get, mock_verify):
        BobcatAPI(hostname=self.mock_hostname, log_level=DISABLED).refresh_dig()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/dig.json")

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.get")
    def test_refresh(self, mock_requests_get, mock_verify):
        BobcatAPI(hostname=self.mock_hostname, log_level=DISABLED).refresh()
        mock_requests_get.assert_has_calls(
            [
                call("http://" + self.mock_hostname + "/status.json"),
                call("http://" + self.mock_hostname + "/miner.json"),
                call("http://" + self.mock_hostname + "/temp.json"),
                call("http://" + self.mock_hostname + "/speed.json"),
                call("http://" + self.mock_hostname + "/dig.json"),
            ],
            any_order=True,
        )

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.post", side_effect=mock_endpoints.mock_online)
    def test_reboot(self, mock_requests_post, mock_verify):
        b = BobcatAPI(hostname=self.mock_hostname, log_level=DISABLED)
        actual_response = b._BobcatAPI__reboot()

        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/reboot",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )
        self.assertEqual(actual_response.text, mock_endpoints.reboot_response_data)

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.post", side_effect=mock_endpoints.mock_online)
    def test_reset(self, mock_requests_post, mock_verify):
        b = BobcatAPI(hostname=self.mock_hostname, log_level=DISABLED)
        actual_response = b._BobcatAPI__reset()

        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/reset",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )
        self.assertEqual(
            actual_response.text,
            mock_endpoints.reset_response_data,
        )

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.post", side_effect=mock_endpoints.mock_online)
    def test_resync(self, mock_requests_post, mock_verify):
        b = BobcatAPI(hostname=self.mock_hostname, log_level=DISABLED)
        actual_response = b._BobcatAPI__resync()

        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/resync",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )
        self.assertEqual(
            actual_response.text,
            mock_endpoints.resync_response_data,
        )

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.post", side_effect=mock_endpoints.mock_online)
    def test_fastsync(self, mock_requests_post, mock_verify):
        b = BobcatAPI(hostname=self.mock_hostname, log_level=DISABLED)
        actual_response = b._BobcatAPI__fastsync()

        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/fastsync",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )
        self.assertEqual(actual_response.text, mock_endpoints.fastsync_response_data)


if __name__ == "__main__":
    unittest.main()
