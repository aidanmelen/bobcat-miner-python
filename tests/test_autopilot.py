from unittest.mock import patch

import unittest

from bobcat_miner import BobcatAutopilot

import mock_bobcat


class TestAutopilot(unittest.TestCase):
    """Test BobcatAutopilot."""

    @patch("requests.get", side_effect=mock_bobcat.mock_synced_bobcat)
    def setUp(self, mock_requests_get, mock_request):
        self.bobcat = BobcatAutopilot(hostname="192.168.0.10", ensure_hostname=False)
        self.bobcat.refresh()


if __name__ == "__main__":
    unittest.main()
