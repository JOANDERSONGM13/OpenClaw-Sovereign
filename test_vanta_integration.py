import os
import json
import time
from brain import BrainRouter

def test_integration():
    print("Testing Vanta Integration...")
    
    # 1. Verify Imports and Class Structure
    try:
        brain = BrainRouter()
        if not hasattr(brain, 'get_market_sentiment'):
            print("❌ BrainRouter missing 'get_market_sentiment' method.")
            return
        print("✅ BrainRouter has 'get_market_sentiment'.")
    except Exception as e:
        print(f"❌ Failed to initialize BrainRouter: {e}")
        return

    # 2. Simulate Signal File
    signal_data = [
        {
            "sequence": 1,
            "miner_hotkey": "5Hb...",
            "trade_pair": "BTCUSD",
            "order_type": "SHORT",
            "leverage": 20.0,
            "price": 65000.0,
            "timestamp": 1715000000000
        }
    ]
    
    with open("vanta_signals.json", "w") as f:
        json.dump(signal_data, f)
    
    print("✅ Created dummy 'vanta_signals.json'.")

    # 3. Test Reading
    sentiment = brain.get_market_sentiment(limit=5)
    print(f"Sentiment Retrieved: {sentiment}")
    
    if len(sentiment) == 1 and "BTCUSD" in sentiment[0]:
        print("✅ Brain successfully read and formatted signals.")
    else:
        print("❌ Brain failed to read signals correctly.")

    # 4. Cleanup
    os.remove("vanta_signals.json")
    print("✅ Cleanup complete.")

if __name__ == "__main__":
    test_integration()
