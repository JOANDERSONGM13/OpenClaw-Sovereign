import os
import sys
import json
import logging
from dotenv import load_dotenv

# Add current directory to path so imports work
sys.path.append(os.getcwd())

try:
    from vanta_api.websocket_client import VantaWebSocketClient
except ImportError as e:
    print(f"Error importing Vanta client: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("VantaObserver")

load_dotenv()

API_KEY = os.getenv("VANTA_API_KEY")

class VantaObserver:
    def __init__(self):
        self.latest_signals = []
        self.api_key = API_KEY

    def handle_messages(self, messages):
        for msg in messages:
            try:
                # msg is a VantaWebSocketMessage object
                # It has .position (Position object) and .new_order (Order object)
                # We want to extract key info
                
                signal = {
                    "sequence": msg.sequence,
                    "miner_hotkey": msg.position.miner_hotkey,
                    "trade_pair": msg.position.trade_pair.trade_pair_id,
                    "order_type": msg.new_order.order_type.name,
                    "leverage": msg.new_order.leverage,
                    "price": msg.new_order.price,
                    "timestamp": msg.timestamp
                }
                
                logger.info(f"CAPTURED SIGNAL: {signal['miner_hotkey'][:8]}... {signal['order_type']} {signal['trade_pair']} x{signal['leverage']}")
                
                self.latest_signals.append(signal)
                # Keep only last 100 signals
                if len(self.latest_signals) > 100:
                    self.latest_signals.pop(0)
                    
                # Save to file for Brain consumption (simple IPC)
                with open("vanta_signals.json", "w") as f:
                    json.dump(self.latest_signals, f, indent=2)
                    
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    def run(self):
        if not self.api_key:
            logger.error("VANTA_API_KEY not found in .env")
            return

        logger.info("Starting Vanta Observer...")
        # Default host/port from config or env
        # vanta_api defaults to localhost:8765. Research showed Request Network uses public endpoints?
        # The README says: "For end users who want to access Vanta data, you will need a Request Network API key."
        # It doesn't explicitly give the WSS URL.
        # But `validator_rest_server.md` mentions `api-ws-port DEFAULT: 8765`.
        # I suspect I need a public URL for the Request Network if I'm not running a local validator.
        # Let's check if there is a known public endpoint.
        # If not, I might need to ask the user or look deeper.
        # However, for now, let's assume valid URL or try to find it.
        # If VANTA_WEBSOCKET_URL is in env, use it.
        
        host = os.getenv("VANTA_WEBSOCKET_HOST", "ws.vanta.dummy") # Placeholder if unknown
        # Actually, let's check `websocket_client.py` defaults. It defaults to localhost.
        
        # User task said: "Research Vanta Repository".
        # I saw `https://request.taoshi.io/login` in README.
        # Maybe the endpoint is `wss://request.taoshi.io` or similar?
        # Let's try to infer or let user provide it.
        
        # For now, I will use a dummy host or localhost and expect it to fail if not running.
        # But wait, checking `websocket_client.py` it constructs URI as `ws://host:port`.
        # If I want `wss://api.vanta.ai`, I need to pass secure=True.
        
        host = os.getenv("VANTA_WEBSOCKET_HOST", "localhost")
        port = int(os.getenv("VANTA_WEBSOCKET_PORT", "8765"))
        secure = os.getenv("VANTA_WEBSOCKET_SECURE", "False").lower() == "true"
        
        client = VantaWebSocketClient(
            api_key=self.api_key, 
            host=host, 
            port=port,
            secure=secure
        )
        
        try:
            client.run(self.handle_messages)
        except KeyboardInterrupt:
            logger.info("Stopping Vanta Observer...")

if __name__ == "__main__":
    observer = VantaObserver()
    observer.run()
