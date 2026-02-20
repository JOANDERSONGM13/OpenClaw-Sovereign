import requests
import json
import time
import sys
import os
from dotenv import load_dotenv

load_dotenv()

GOPHER_API_KEY = os.getenv("GOPHER_API_KEY")
BASE_URL = "https://data.gopher-ai.com/api/v1"

def poll_gopher(job_id, interval=5, timeout=60):
    """
    Polls the Gopher API for job completion.
    """
    url = f"{BASE_URL}/search/live/result/{job_id}"
    headers = {"Authorization": f"Bearer {GOPHER_API_KEY}"}
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            print(f"Polling {url}...")
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                     print("\nJob Completed!")
                     # Print first item to avoid massive log
                     if len(data) > 0:
                         print(json.dumps(data[0], indent=2))
                         print(f"... and {len(data)-1} more items.")
                     else:
                         print("[] (Empty result)")
                     return data

                status = data.get("status")
                
                if status == "in progress":
                    print("Job still in progress...")
                elif status == "completed" or "result" in data: # Check for success indicators
                     print("\nJob Completed!")
                     print(json.dumps(data, indent=2))
                     return data
                elif status == "failed":
                    print(f"Job Failed: {data.get('error')}")
                    return None
                else:
                    # If the structure is different, print what we got
                    print(f"Unknown status or completed: {data}")
                    return data
            else:
                print(f"Request failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"Polling error: {e}")
            
        time.sleep(interval)
    
    print("Polling timed out.")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 poll_gopher.py <JOB_UUID>")
        sys.exit(1)
    
    job_uuid = sys.argv[1]
    poll_gopher(job_uuid)
