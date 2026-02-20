from stealth_browser import StealthBrowser
import os
from dotenv import load_dotenv

load_dotenv()

def test_stealth_browser():
    print("Testing RedTeam (SN61) Stealth Browser...")
    browser = StealthBrowser()
    
    # Check Profile
    profile = browser.get_profile()
    print(f"\n[Profile Loaded]:")
    print(f"User-Agent: {profile.get('headers', {}).get('User-Agent', 'N/A')[:50]}...")
    
    # Check Request
    target = "https://httpbin.org/headers"
    print(f"\n[Browsing]: {target}")
    try:
        resp = browser.browse(target)
        print(f"Status: {resp.status_code}")
        print("Response Headers seen by server:")
        print(resp.text)
    except Exception as e:
        print(f"Browsing failed: {e}")

if __name__ == "__main__":
    test_stealth_browser()
