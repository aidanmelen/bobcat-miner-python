from unittest.mock import patch
from unittest.mock import call

import unittest

from bobcat_miner import BobcatAPI

DISABLED = 100


class TestBobcatAPI(unittest.TestCase):
    """Test BobcatAPI."""

    def setUp(self):
        self.mock_hostname = "192.168.0.10"
        self.mock_response = "mocked response text"

    @patch("requests.get")
    def test_refresh_status(self, mock_requests_get):
        b = BobcatAPI(hostname=self.mock_hostname, ensure_hostname=False, log_level=DISABLED)
        b.refresh_status()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/status.json")

    @patch("requests.get")
    def test_refresh_miner(self, mock_requests_get):
        b = BobcatAPI(hostname=self.mock_hostname, ensure_hostname=False, log_level=DISABLED)
        b.refresh_miner()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/miner.json")

    @patch("requests.get")
    def test_refresh_temp(self, mock_requests_get):
        b = BobcatAPI(hostname=self.mock_hostname, ensure_hostname=False, log_level=DISABLED)
        b.refresh_temp()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/temp.json")

    @patch("requests.get")
    def test_refresh_speed(self, mock_requests_get):
        b = BobcatAPI(hostname=self.mock_hostname, ensure_hostname=False, log_level=DISABLED)
        b.refresh_speed()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/speed.json")

    @patch("requests.get")
    def test_refresh_dig(self, mock_requests_get):
        b = BobcatAPI(hostname=self.mock_hostname, ensure_hostname=False, log_level=DISABLED)
        b.refresh_dig()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/dig.json")

    @patch("requests.get")
    def test_refresh(self, mock_requests_get):
        b = BobcatAPI(hostname=self.mock_hostname, ensure_hostname=False, log_level=DISABLED)
        b.refresh()
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

    @patch("requests.post")
    def test_reboot(self, mock_requests_post):
        mock_requests_post.return_value.text = self.mock_response

        b = BobcatAPI(hostname=self.mock_hostname, ensure_hostname=False, log_level=DISABLED)
        actual_response = b.reboot()

        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/reboot",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )
        self.assertEqual(actual_response, self.mock_response)

    @patch("requests.post")
    def test_reset(self, mock_requests_post):
        mock_requests_post.return_value.text = self.mock_response

        b = BobcatAPI(hostname=self.mock_hostname, ensure_hostname=False, log_level=DISABLED)
        actual_response = b.reset()

        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/reset",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )
        self.assertEqual(actual_response, self.mock_response)

    @patch("requests.post")
    def test_resync(self, mock_requests_post):
        mock_requests_post.return_value.text = self.mock_response

        b = BobcatAPI(hostname=self.mock_hostname, ensure_hostname=False, log_level=DISABLED)
        actual_response = b.resync()

        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/resync",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )
        self.assertEqual(actual_response, self.mock_response)

    @patch("requests.post")
    def test_fastsync(self, mock_requests_post):
        mock_requests_post.return_value.text = self.mock_response

        b = BobcatAPI(hostname=self.mock_hostname, ensure_hostname=False, log_level=DISABLED)
        actual_response = b.fastsync()

        mock_requests_post.assert_called_once_with(
            "http://" + self.mock_hostname + "/admin/fastsync",
            headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"},
        )
        self.assertEqual(actual_response, self.mock_response)


if __name__ == "__main__":
    unittest.main()
