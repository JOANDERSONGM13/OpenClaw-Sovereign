from brain import BrainRouter
import sys
import json

def main():
    if len(sys.argv) < 2:
        url = "https://example.com"
        print(f"No URL provided. Using default: {url}")
    else:
        url = sys.argv[1]

    print("Initializing BrainRouter (v2.2)...")
    brain = BrainRouter()
    
    print(f"\n🧠 BRAIN: Searching/Scraping: {url}")
    results = brain.search_web(url)
    
    if results:
        print(f"\n✅ Result Found! ({len(results)} items)")
        # Print the first result's content snippet
        first_item = results[0]
        content = first_item.get("content", "")
        print("\n--- Content Snippet ---")
        print(content[:500] + "..." if len(content) > 500 else content)
        print("-----------------------")
        print(f"\nFull Metadata: {first_item.get('metadata')}")
    else:
        print("\n❌ No results found or error occurred.")

if __name__ == "__main__":
    main()
