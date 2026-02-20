import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GOPHER_API_KEY")
url = "https://data.gopher-ai.com/api/v1/search/live"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "type": "twitter",
    "arguments": {
        "type": "searchbyquery",
        "query": "from:gopher_ai",
        "max_results": 2
    }
}

print("\n--- Testing Gopher API ---")
try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        # Print FULL structure to understand how to parse
        print(json.dumps(data, indent=2)) 
    else:
        print(f"Failed: {response.text}")

except Exception as e:
    print(f"Request failed: {e}")
