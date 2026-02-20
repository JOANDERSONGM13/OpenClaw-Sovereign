import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import MagicMock, patch
from brain import BrainRouter

class TestSecureRouting(unittest.TestCase):
    @patch('brain.Client')
    @patch('brain.StealthBrowser')
    @patch('brain.BitsecAuditor')
    @patch('brain.GopherClient')
    @patch('brain.HandshakeConsultant')
    @patch('brain.SoulManager')
    @patch('brain.ContextLoader')
    @patch('brain.GittensorClient')
    @patch('brain.MacrocosmClient')
    @patch('brain.AffineClient')
    @patch('brain.TaoshiClient')
    @patch('brain.ManakoVision')
    def setUp(self, *args):
        # Mock environment variables to ensure clients are initialized
        with patch.dict(os.environ, {
            "CHUTES_API_KEY": "mock_key",
            "TARGON_API_KEY": "mock_key"
        }):
            self.brain = BrainRouter()

    def test_think_secure_routing(self):
        # Mock the Chutes client response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Secure response"
        self.brain.chutes_client.chat.completions.create.return_value = mock_response

        # Call think with is_sensitive=True
        result = self.brain.think("my secret password", is_sensitive=True)

        # Verify Chutes was called with the TEE model
        self.brain.chutes_client.chat.completions.create.assert_called()
        call_args = self.brain.chutes_client.chat.completions.create.call_args
        self.assertEqual(call_args.kwargs['model'], "chutes/kimi-k2.5-tee")
        self.assertEqual(result, "Secure response")

    def test_think_normal_routing(self):
         # Mock the Chutes client response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Normal response"
        self.brain.chutes_client.chat.completions.create.return_value = mock_response
        
        # Test normal low complexity prompt
        result = self.brain.think("hello world", is_sensitive=False)
        
        # Verify Chutes was called with default/env model (not TEE specific unless env is set)
        call_args = self.brain.chutes_client.chat.completions.create.call_args
        # The default model logic uses getenv, so we check it's not the tee model forced by logic
        current_model_arg = call_args.kwargs['model']
        self.assertNotEqual(current_model_arg, "chutes/kimi-k2.5-tee")
        self.assertEqual(result, "Normal response")

if __name__ == '__main__':
    unittest.main()
