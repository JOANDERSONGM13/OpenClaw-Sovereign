import requests
import json
import time
import os
from dotenv import load_dotenv

class GopherClient:
    """
    Client for Gopher (Subnet 42) - Data Scraping & Search.
    """
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOPHER_API_KEY")
        self.base_url = "https://data.gopher-ai.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def scrape(self, url: str, max_pages: int = 3, max_depth: int = 1, wait: bool = True):
        """
        Starts a scraping job and optionally waits for the result.
        """
        if not self.api_key:
            print("[Gopher] API Key missing.")
            return None

        # 1. Submit Job
        submit_url = f"{self.base_url}/search/live"
        payload = {
            "type": "web",
            "arguments": {
                "type": "scraper",
                "url": url,
                "max_pages": max_pages,
                "max_depth": max_depth
            }
        }
        
        try:
            print(f"[Gopher] Submitting scrape job for {url}...")
            resp = requests.post(submit_url, json=payload, headers=self.headers, timeout=10)
            if resp.status_code != 200:
                print(f"[Gopher] Submission failed: {resp.text}")
                return None
                
            job_data = resp.json()
            job_id = job_data.get("uuid")
            if not job_id:
                print(f"[Gopher] No Job ID returned: {job_data}")
                return None
                
            print(f"[Gopher] Job started: {job_id}")
            
            if wait:
                return self._poll_result(job_id)
            return job_id
            
        except Exception as e:
            print(f"[Gopher] Error: {e}")
            return None

    def _poll_result(self, job_id: str, timeout: int = 120):
        """
        Polls for the result of a specific job.
        """
        poll_url = f"{self.base_url}/search/live/result/{job_id}"
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                resp = requests.get(poll_url, headers=self.headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    
                    # If data is a list, it means success (the results)
                    if isinstance(data, list):
                        return data
                        
                    status = data.get("status")
                    
                    if status == "completed" or "result" in data:
                        # Success!
                        return data
                    elif status == "failed":
                        print(f"[Gopher] Job failed: {data.get('error')}")
                        return None
                    # else in progress, continue
                elif resp.status_code == 404:
                     # Sometimes it takes a moment to propagate?
                     pass
                else:
                    print(f"[Gopher] Poll error: {resp.status_code}")
                    
            except Exception as e:
                print(f"[Gopher] Poll exception: {e}")
                
            time.sleep(3) # Wait 3s between checks
            
        print("[Gopher] Operation timed out.")
        return None

if __name__ == "__main__":
    # Test
    client = GopherClient()
    # Test with a very small/fast site if possible, or just check init
    print("GopherClient initialized.")
