import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GOPHER_API_KEY")
base_url = "https://data.gopher-ai.com/api/v1"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 1. Start the Job
print("\n--- Starting Search Job ---")
start_url = f"{base_url}/search/live"
payload = {
    "type": "twitter",
    "arguments": {
        "type": "searchbyquery",
        "query": "from:gopher_ai",
        "max_results": 2
    }
}

try:
    response = requests.post(start_url, headers=headers, json=payload)
    data = response.json()
    job_id = data.get("uuid")
    
    if not job_id:
        print("Failed to get UUID. Exiting.")
        print(data)
        exit(1)
        
    print(f"Got Job ID: {job_id}")
    
    # 2. Test Alternatives
    alternatives = [
        {"method": "GET", "url": f"{base_url}/tasks/{job_id}"},
        {"method": "GET", "url": f"{base_url}/status/{job_id}"},
        {"method": "GET", "url": f"{base_url}/requests/{job_id}"},
        {"method": "POST", "url": f"{base_url}/jobs/{job_id}"}, # Maybe POST to refresh?
        {"method": "GET", "url": f"https://api.gopher-ai.com/v1/jobs/{job_id}"}, # Different host?
    ]
    
    print("\n--- Testing Alternatives ---")
    time.sleep(2) 
    
    for alt in alternatives:
        print(f"Testing {alt['method']} {alt['url']}...")
        try:
            if alt['method'] == "GET":
                resp = requests.get(alt['url'], headers=headers)
            else:
                resp = requests.post(alt['url'], headers=headers)
            
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                print(">>> SUCCESS! <<<")
                print(resp.text[:200])
                break
        except Exception as e:
            print(f"Failed: {e}")

except Exception as e:
    print(f"Request failed: {e}")
