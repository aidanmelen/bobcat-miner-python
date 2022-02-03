from unittest.mock import patch, AsyncMock

import asyncio
import unittest

from bobcat_miner import BobcatConnection

DISABLED = 100


class TestBobcatConnection(unittest.TestCase):
    """Test BobcatConnection."""

    def setUp(self):
        self.mock_hostname = "192.168.0.10"

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    def test_BobcatConnection_with_hostname(self, mock_verify):
        mock_verify.return_value = (True, self.mock_hostname)
        self.mock_verify = mock_verify

        _ = BobcatConnection(hostname=self.mock_hostname)
        mock_verify.assert_awaited_with(self.mock_hostname)

    @patch("bobcat_miner.BobcatConnection.find")
    def test_BobcatConnection_without_hostname(self, mock_find):
        _ = BobcatConnection()
        mock_find.assert_called_once_with()

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.get")
    def test_refresh_miner_with_hostname(self, mock_requests_get, mock_verify):
        mock_hostname_override = "192.168.0.20"
        b = BobcatConnection(hostname=self.mock_hostname)
        b._BobcatConnection__refresh_miner(hostname=mock_hostname_override)
        mock_requests_get.assert_called_once_with(
            "http://" + mock_hostname_override + "/miner.json"
        )

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("requests.get")
    def test_refresh_miner_without_hostname(self, mock_requests_get, mock_verify):
        b = BobcatConnection(hostname=self.mock_hostname)
        b._BobcatConnection__refresh_miner()
        mock_requests_get.assert_called_once_with("http://" + self.mock_hostname + "/miner.json")


    @patch("bobcat_miner.BobcatConnection.find")
    @patch("bobcat_miner.BobcatConnection._BobcatConnection__get_homepage", return_value=AsyncMock())
    @patch("bobcat_miner.BobcatConnection._BobcatConnection__does_bobcat_match_animal")
    def test_verify_should_pass(self, mock_does_bobcat_match_animal, mock_get_homepage, mock_find):
        mock_get_homepage.return_value = "Diagnoser - Bobcatminer Diagnostic Dashboard"
        b = BobcatConnection()
        is_bobcat_verified, host = asyncio.run(b.verify(self.mock_hostname))

        mock_get_homepage.assert_awaited_with(self.mock_hostname)
        self.assertFalse(mock_does_bobcat_match_animal.called)
        
        self.assertTrue(is_bobcat_verified)
        self.assertEqual(host, self.mock_hostname)
    
    @patch("bobcat_miner.BobcatConnection.find")
    @patch("bobcat_miner.BobcatConnection._BobcatConnection__get_homepage", return_value=AsyncMock())
    @patch("bobcat_miner.BobcatConnection._BobcatConnection__does_bobcat_match_animal")
    def test_verify_should_fail(self, mock_does_bobcat_match_animal, mock_get_homepage, mock_find):
        mock_get_homepage.return_value = "This is not a bobcat"
        b = BobcatConnection()
        is_bobcat_verified, host = asyncio.run(b.verify(self.mock_hostname))

        mock_get_homepage.assert_awaited_with(self.mock_hostname)
        self.assertFalse(mock_does_bobcat_match_animal.called)
        
        self.assertFalse(is_bobcat_verified)
        self.assertEqual(host, self.mock_hostname)


    @patch("bobcat_miner.BobcatConnection.find")
    @patch("bobcat_miner.BobcatConnection._BobcatConnection__get_homepage", return_value=AsyncMock())
    @patch("bobcat_miner.BobcatConnection._BobcatConnection__does_bobcat_match_animal")
    def test_verify_with_animal_match(self, mock_does_bobcat_match_animal, mock_get_homepage, mock_find):
        mock_get_homepage.return_value = "Diagnoser - Bobcatminer Diagnostic Dashboard"
        b = BobcatConnection(animal="fancy-awesome-bobcat")
        b._animal = "fancy-awesome-bobcat"
        is_bobcat_verified, host = asyncio.run(b.verify(self.mock_hostname))
        mock_does_bobcat_match_animal.assert_called_once_with(self.mock_hostname)

        self.assertTrue(is_bobcat_verified)
        self.assertEqual(host, self.mock_hostname)

    # @patch("bobcat_miner.BobcatConnection.find")
    # @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    # def test_BobcatConnection(self, mock_verify, mock_find):
    #     _ = BobcatConnection(hostname=self.mock_hostname)
    #     mock_verify.assert_awaited_with(self.mock_hostname)

    #     _ = BobcatConnection()
    #     mock_find.assert_called_once_with()

    @patch("bobcat_miner.BobcatConnection.verify", return_value=AsyncMock())
    @patch("socket.socket.connect")
    def test_can_connect(self, mock_socket_connect, mock_verify):
        b = BobcatConnection(hostname=self.mock_hostname)
        self.assertTrue(b.can_connect())
        mock_socket_connect.assert_called_once_with((self.mock_hostname, 80))


if __name__ == "__main__":
    unittest.main()
