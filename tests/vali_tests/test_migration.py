import unittest
import sys
from unittest.mock import MagicMock, patch

# Mock collateral_sdk before importing ValidatorContractManager
sys.modules['collateral_sdk'] = MagicMock()
sys.modules['pandas_market_calendars'] = MagicMock()

sys.modules['collateral_sdk'] = MagicMock()
sys.modules['pandas_market_calendars'] = MagicMock()
sys.modules['template'] = MagicMock()
sys.modules['template.protocol'] = MagicMock()
sys.modules['shared_objects'] = MagicMock()
sys.modules['shared_objects.rpc'] = MagicMock()
sys.modules['shared_objects'] = MagicMock()
sys.modules['shared_objects.rpc'] = MagicMock()
sys.modules['shared_objects.rpc.rpc_client_base'] = MagicMock()
sys.modules['shared_objects.sn8_multiprocessing'] = MagicMock()
sys.modules['scipy'] = MagicMock()
sys.modules['scipy.stats'] = MagicMock()

from vali_objects.contract.validator_contract_manager import ValidatorContractManager
from vali_objects.vali_config import ValiConfig
from vali_objects.miner_account.miner_account_manager import MinerAccount
from vali_objects.vali_dataclasses.position import Position
from vali_objects.vali_dataclasses.order import Order
from vali_objects.enums.order_type_enum import OrderType
from vali_objects.vali_config import TradePair

class TestMigration(unittest.TestCase):
    def setUp(self):
        self.mock_config = MagicMock()
        self.mock_config.subtensor.network = "test"
        self.manager = ValidatorContractManager(config=self.mock_config, running_unit_tests=True, connection_mode=0)
        
        # Mock dependencies
        self.manager.metagraph = MagicMock()
        self.manager.metagraph.hotkeys = ["miner1"]
        self.manager._miner_account_client = MagicMock()
        self.manager._position_client = MagicMock()
        self.manager._set_miner_account_size = MagicMock()
        
    def test_rebuild_accounts_with_open_positions(self):
        # Setup mock account
        mock_account = {"capital_used": 0.0}
        self.manager._miner_account_client.get_account.return_value = mock_account
        
        # Setup mock position
        mock_position = MagicMock(spec=Position)
        mock_position.net_quantity = 1.0
        mock_position.average_entry_price = 50000.0
        # Determine exact lot size for BTCUSD/Crypto
        mock_position.trade_pair = TradePair.BTCUSD
        mock_position.orders = [MagicMock(quote_usd_rate=1.0)]
        
        # calculate expected capital used: 1.0 * 50000.0 * 1 * 1.0 = 50000.0
        
        self.manager._position_client.get_all_miner_positions.return_value = [mock_position]
        
        # Run migration
        self.manager.rebuild_miner_accounts_cpt_2026()
        
        # Verify force_update_capital_used was called with correct value
        self.manager._miner_account_client.force_update_capital_used.assert_called_with("miner1", 50000.0)
        
    def test_rebuild_accounts_no_positions(self):
        self.manager._position_client.get_all_miner_positions.return_value = []
        self.manager.rebuild_miner_accounts_cpt_2026()
        # Should not call force update if 0
        self.manager._miner_account_client.force_update_capital_used.assert_not_called()

if __name__ == '__main__':
    unittest.main()
