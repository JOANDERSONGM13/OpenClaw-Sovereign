import requests
import sys

def check_endpoint(url):
    print(f"Checking {url}...")
    try:
        # Use stream=True to handle SSE
        with requests.get(url, stream=True, timeout=5) as response:
            print(f"Status: {response.status_code}")
            print(f"Headers: {response.headers}")
            content_type = response.headers.get("Content-Type", "")
            
            if "text/event-stream" in content_type:
                print(">>> SUCCESS: Detected SSE Endpoint! <<<")
                return True
            else:
                print(f"Content-Type: {content_type} (Not SSE)")
                return False
    except Exception as e:
        print(f"Failed: {e}")
        return False

endpoints = [
    "https://mcp.taostats.io/sse",
    "https://mcp.taostats.io/api/sse",
    "https://mcp.taostats.io/v1/sse",
    "https://mcp.taostats.io",
]

print("--- Probing Taostats MCP Endpoints ---")
for ep in endpoints:
    if check_endpoint(ep):
        break
    print("-" * 20)
