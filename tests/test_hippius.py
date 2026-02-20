import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from src.memory.hippius_vault import HippiusVault

class TestHippiusVault(unittest.TestCase):
    @patch('src.memory.hippius_vault.requests.post')
    def test_upload_file(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {"file_hash": "QmHash123"}
        mock_post.return_value = mock_response

        vault = HippiusVault()
        result = vault.upload_file("test.txt", b"content")
        
        self.assertEqual(result, "QmHash123")
        mock_post.assert_called_with(
            "https://api.hippius.tao/v1/storage/upload",
            files={'file': ("test.txt", b"content")},
            headers={"Authorization": "Bearer None"}
        )

if __name__ == '__main__':
    unittest.main()
