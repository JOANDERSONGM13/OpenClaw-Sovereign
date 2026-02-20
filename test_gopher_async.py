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
    print(f"Start Response: {json.dumps(data, indent=2)}")
    
    job_id = data.get("uuid")
    if not job_id:
        print("Failed to get UUID. Exiting.")
        exit(1)
        
    print(f"\nGot Job ID: {job_id}")
    
    # 2. Poll for Results
    # Guessing endpoint structure based on common patterns
    poll_endpoints = [
        f"{base_url}/jobs/{job_id}",
        f"{base_url}/search/live/{job_id}",
        f"{base_url}/result/{job_id}"
    ]
    
    for i in range(3):
        print(f"\n--- Polling Attempt {i+1} ---")
        time.sleep(2) # Wait a bit
        
        for poll_url in poll_endpoints:
            print(f"Checking: {poll_url}")
            try:
                poll_resp = requests.get(poll_url, headers=headers)
                print(f"Status: {poll_resp.status_code}")
                if poll_resp.status_code == 200:
                    result_data = poll_resp.json()
                    print(">>> SUCCESS: Got Result! <<<")
                    print(json.dumps(result_data, indent=2)[:500] + "...")
                    exit(0)
            except Exception as e:
                print(f"Poll failed: {e}")

except Exception as e:
    print(f"Request failed: {e}")
