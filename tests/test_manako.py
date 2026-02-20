import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from src.tools.manako_vision import ManakoVision

class TestManakoVision(unittest.TestCase):
    @patch('src.tools.manako_vision.requests.post')
    def test_look_at_image(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {"description": "A cat sitting on a mat"}
        mock_post.return_value = mock_response

        vision = ManakoVision()
        result = vision.look_at("http://example.com/cat.jpg")
        
        self.assertIn("👁️ Visão Manako: A cat sitting on a mat", result)
        mock_post.assert_called_with(
            "https://api.manako.tao/v1/visual-search/image_captioning",
            json={"url": "http://example.com/cat.jpg"},
            headers={"Authorization": "Bearer None"}
        )

    @patch('src.tools.manako_vision.requests.post')
    def test_look_at_video_query(self, mock_post):
        # Mock response for video search
        mock_response = MagicMock()
        mock_response.json.return_value = {"timestamp": "00:45"}
        mock_post.return_value = mock_response

        vision = ManakoVision()
        result = vision.look_at("http://example.com/match.mp4", query="GOAL")
        
        self.assertIn("👁️ Visão Manako: 00:45", result)
        mock_post.assert_called_with(
            "https://api.manako.tao/v1/visual-search/video_search",
            json={"url": "http://example.com/match.mp4", "query": "GOAL"},
            headers={"Authorization": "Bearer None"}
        )

if __name__ == '__main__':
    unittest.main()
