import os
import shutil
from brain import BrainRouter

def test_trajectory():
    print("Testing TrajectoryRL (SN11) Integration...")
    
    # Clean up previous soul if exists to test generation
    if os.path.exists("SOUL.md"):
        os.remove("SOUL.md")
        print("🗑️ Removed existing SOUL.md")

    print("🧠 Initializing BrainRouter (triggers SoulManager)...")
    brain = BrainRouter()
    
    # 1. Verify SOUL.md generation
    if os.path.exists("SOUL.md"):
        print("✅ SOUL.md successfully generated from Academy.")
    else:
        print("❌ SOUL.md failed to generate.")
        return

    # 2. Verify Content
    with open("SOUL.md", "r") as f:
        content = f.read()
        
    if "OpenClaw" in content and "Traits" in content:
        print("✅ SOUL.md contains correct Personality data.")
    else:
        print("❌ SOUL.md content unexpected.")

    # 3. Verify Brain Logic
    if "OpenClaw" in brain.system_prompt:
        print("✅ BrainRouter loaded system prompt correctly.")
    else:
        print("❌ BrainRouter system prompt mismatch.")
        
    print("\n[Current Soul Preview]")
    print(content[:300] + "...")

if __name__ == "__main__":
    test_trajectory()
