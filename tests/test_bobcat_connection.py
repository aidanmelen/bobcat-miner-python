from unittest.mock import patch

import unittest

from bobcat_miner import BobcatConnection

DISABLED = 100


class TestBobcatConnection(unittest.TestCase):
    """Test BobcatConnection."""

    def setUp(self):
        self.mock_hostname = "192.168.0.10"

    @patch("socket.socket.connect")
    def test_can_connect(self, mock_socket_connect):
        b = BobcatConnection(hostname=self.mock_hostname, ensure_hostname=False, log_level=DISABLED)
        self.assertTrue(b.can_connect())
        mock_socket_connect.assert_called_once_with((self.mock_hostname, 80))


if __name__ == "__main__":
    unittest.main()
