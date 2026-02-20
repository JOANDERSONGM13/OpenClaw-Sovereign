from mcp_client import MCPClient
import os
import time
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("TAOSTATS_MCP_URL")

if not url:
    print("TAOSTATS_MCP_URL not set")
    exit(1)

client = MCPClient(url)
if client.connect():
    time.sleep(1)
    
    # Try getting Stats first (general)
    # Then try GetLatestSubnetPool for netuid 33
    
    print("\n--- Querying Subnet 33 Metrics ---\n")
    client.call_tool("GetLatestSubnetPool", {"netuid": 33})
    
    # Keep alive briefly to get response
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        pass
else:
    print("Failed to connect")
