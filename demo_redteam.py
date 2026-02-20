from brain import BrainRouter
import sys
import json

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "https://httpbin.org/headers"
    
    print("Initializing BrainRouter (v2.2)...")
    brain = BrainRouter()
    
    print(f"\n🕵️ REDTEAM: Stealth Browsing to {target}")
    print("This will use a randomized browser fingerprint from Subnet 61.")
    
    response = brain.browse(target)
    
    if response and response.status_code == 200:
        print(f"\n✅ Success! (Status: {response.status_code})")
        print("\n--- Server Identification (How the server sees us) ---")
        try:
            data = response.json()
            print(json.dumps(data, indent=2))
        except:
            print(response.text[:500])
        print("------------------------------------------------------")
    else:
        print(f"\n❌ Request failed: {response.status_code if response else 'None'}")

if __name__ == "__main__":
    main()
