import requests
import json
import threading
import time
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any

class MCPClient:
    """
    MCP Client for Taostats:
    1. POST initialize (keep open as SSE stream).
    2. Capture Session ID from headers.
    3. Send other RPCs via separate POSTs to ?sessionId=...
    """
    def __init__(self, full_url: str):
        self.api_key = self._extract_key(full_url)
        # Base URL is the root
        self.base_url = "https://mcp.taostats.io/"
        
        self.session_id: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": self.api_key,
            "Accept": "application/json, text/event-stream", # Vital for the stream
            "Content-Type": "application/json"
        })
        
        self.ready = False
        self._stop_event = threading.Event()

    def _extract_key(self, url: str) -> str:
        if "api_key=" in url:
            return url.split("api_key=")[1].split("&")[0]
        elif "apikey=" in url:
            return url.split("apikey=")[1].split("&")[0]
        return ""

    def connect(self):
        """Starts the SSE stream via 'initialize'."""
        print(f"Connecting to {self.base_url} (Key: {self.api_key[:5]}...)")
        
        # We start the listener thread which will perform the blocking POST
        self._thread = threading.Thread(target=self._connect_and_listen, daemon=True)
        self._thread.start()
        
        # Wait for Session ID
        print("Waiting for Session ID...")
        start_time = time.time()
        while not self.session_id:
            if time.time() - start_time > 10:
                print("Timeout waiting for Session ID.")
                return False
            time.sleep(0.1)
            
        print(f"Got Session ID: {self.session_id}")
        
        # Now we can send the next notification
        self._send_rpc("notifications/initialized", None, id=None)
        self.ready = True
        return True

    def _connect_and_listen(self):
        """Performs the long-polling POST for initialize."""
        payload = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05", # Updated spec
                "capabilities": {},
                "clientInfo": {"name": "openclaw", "version": "1.0"}
            },
            "id": 1
        }
        
        try:
            # This POST opens the stream
            with self.session.post(self.base_url, json=payload, stream=True, timeout=60) as r:
                if r.status_code != 200:
                    print(f"Stream Failed: {r.status_code} - {r.text}")
                    return

                # Capture Session ID from headers
                for k, v in r.headers.items():
                    if k.lower() == "mcp-session-id":
                        self.session_id = v
                        break
                
                # If not in headers, maybe in body?
                # Listen to stream
                for line in r.iter_lines():
                    if self._stop_event.is_set(): break
                    if line:
                        decoded = line.decode('utf-8')
                        print(f"STREAM: {decoded}")
                        if decoded.startswith("data: "):
                            self._handle_data(decoded[6:])
                            
        except Exception as e:
            print(f"Stream Error: {e}")

    def _handle_data(self, data_str, print_output=True):
        try:
            msg = json.loads(data_str)
            if "result" in msg:
                # print(f"RPC Result: {msg}")
                if "tools" in msg["result"]:
                    if print_output:
                        print("\n=== AVAILABLE TOOLS ===")
                        for tool in msg["result"]["tools"]:
                            print(f"- {tool['name']}: {tool.get('description', '')[:80]}...")
                        print("-----------------------")
                    return msg["result"]
                else:
                    # Generic result (e.g. from tool call)
                    # Check for nested JSON in content
                    result = msg["result"]
                    if "content" in result and isinstance(result["content"], list):
                         for item in result["content"]:
                             if item.get("type") == "text" and isinstance(item.get("text"), str):
                                 try:
                                     text = item["text"]
                                     if text.lstrip().startswith(("{", "[")):
                                         item["text"] = json.loads(text)
                                 except:
                                     pass
                    
                    if print_output:
                        print(f"\n[RPC RESULT]: {json.dumps(result, indent=2)}\n")
                    return result
        except:
            pass
        return None

    def _send_rpc(self, method, params=None, id=None):
        """Sends a separate POST request and returns the parsed result."""
        if not self.session_id:
            print("Cannot send: No Session ID")
            return None

        # Add sessionId query param redundantly
        url = f"{self.base_url}?sessionId={self.session_id}"
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {}
        }
        if id is not None:
            payload["id"] = id
        
        try:
            # Add Mcp-Session-Id header
            headers = self.session.headers.copy()
            headers["Mcp-Session-Id"] = self.session_id
            
            # The server returns the result directly in the response body, formatted as SSE
            r = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if r.status_code not in [200, 202]:
                print(f"RPC Send Failed: {r.status_code} - {r.text}")
                return None

            # Parse SSE from response and accumulate result
            accumulated_result = None
            
            for line in r.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith("data: "):
                        # We use a modified handle_data that returns the result
                        res = self._handle_data(decoded[6:], print_output=False)
                        if res:
                            accumulated_result = res
            
            return accumulated_result
                        
        except Exception as e:
            print(f"RPC Send Error: {e}")
            return None

    def list_tools(self):
        print("Requesting tool list...")
        self._send_rpc("tools/list", {}, id=2)

    def call_tool(self, name: str, arguments: Dict[str, Any]):
        """Calls a tool and returns the result."""
        # print(f"Calling tool: {name} with args: {arguments}")
        # ID 3 for calls
        return self._send_rpc("tools/call", {
            "name": name,
            "arguments": arguments
        }, id=3)

if __name__ == "__main__":
    load_dotenv()
    url = os.getenv("TAOSTATS_MCP_URL")
    if url:
        client = MCPClient(url)
        if client.connect():
            time.sleep(1)
            client.list_tools()
            try:
                while True: time.sleep(1)
            except KeyboardInterrupt:
                pass
    else:
        print("Set TAOSTATS_MCP_URL")
