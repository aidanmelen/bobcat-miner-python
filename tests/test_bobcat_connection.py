from unittest.mock import patch, AsyncMock

import unittest

from bobcat_miner import BobcatConnection

DISABLED = 100


class TestBobcatConnection(unittest.TestCase):
    """Test BobcatConnection."""

    @patch("bobcat_miner.BobcatConnection.search")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat", return_value=AsyncMock())
    def setUp(self, mock_bobcat_conn_is_bobcat, mock_bobcat_conn_search):
        self.mock_bobcat_conn_is_bobcat = mock_bobcat_conn_is_bobcat
        self.mock_bobcat_conn_search = mock_bobcat_conn_search
        self.mock_hostname = "192.168.0.10"
        self.bobcat_conn = BobcatConnection(hostname=self.mock_hostname)

    @patch("bobcat_miner.BobcatConnection.search")
    @patch("bobcat_miner.BobcatConnection.is_a_bobcat", return_value=AsyncMock())
    def test_BobcatConnection(self, mock_bobcat_conn_is_bobcat, mock_bobcat_conn_search):
        _ = BobcatConnection(hostname=self.mock_hostname)
        mock_bobcat_conn_is_bobcat.assert_awaited_with(self.mock_hostname)

        _ = BobcatConnection()
        mock_bobcat_conn_search.assert_called_once_with()

    @patch("socket.socket.connect")
    def test_can_connect(self, mock_socket_connect):
        self.assertTrue(self.bobcat_conn.can_connect())
        mock_socket_connect.assert_called_once_with((self.mock_hostname, 80))

    # @patch('aiohttp.ClientSession', return_value=AsyncMock())
    # def test_is_bobcat(self, mock_session):

    #     # mock_session.return_value.__aenter__.get.return_value.__aenter__.return_value.text = "mock content"
    #     self.bobcat_conn.is_a_bobcat(self.mock_hostname)


if __name__ == "__main__":
    unittest.main()
