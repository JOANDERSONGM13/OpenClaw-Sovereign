from vali_objects.price_fetcher.live_price_fetcher import LivePriceFetcher
from vali_objects.vali_config import TradePair
from unittest.mock import MagicMock

# Mock secrets
secrets = {"tiingo_apikey": "dummy", "polygon_apikey": "dummy"}
# Initialize fetcher (this sets polygon to None internally due to our change)
fetcher = LivePriceFetcher(secrets, disable_ws=True, running_unit_tests=True)

print(f"Polygon Service: {fetcher.polygon_data_service}")
assert fetcher.polygon_data_service is None

# Test fallbacks
print("Testing is_market_open fallback...")
try:
    # Use a pair
    fetcher.is_market_open(TradePair.BTCUSD)
    print("is_market_open passed")
except Exception as e:
    print(f"is_market_open failed: {e}")

print("Testing get_currency_conversion fallback...")
try:
    res = fetcher.get_currency_conversion("BTC", "USD")
    print(f"get_currency_conversion result: {res}")
except Exception as e:
    print(f"get_currency_conversion failed: {e}")

print("Testing unified_candle_fetcher fallback...")
try:
    res = fetcher.unified_candle_fetcher(TradePair.BTCUSD, 0, 0)
    print(f"unified_candle_fetcher result: {res}")
except Exception as e:
    print(f"unified_candle_fetcher failed: {e}")
