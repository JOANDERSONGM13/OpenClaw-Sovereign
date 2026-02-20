from ridges import RidgesGenerator

def test_ridges_security():
    print("Testing Ridges (SN62) ADA v2 Compliance...")
    
    generator = RidgesGenerator()
    url = "https://bot-detection.com"
    instruction = "Check if I am detected as a bot."
    
    script = generator.generate_script(url, instruction)
    
    print("\n[Generated Script Sample]\n" + script[:200] + "...\n")
    
    # Verification Checks
    checks = [
        "webdriver.Chrome",
        "--disable-blink-features=AutomationControlled",
        "navigator.webdriver",
        "disable-dev-shm-usage",
        "deviceMemory",
        "hardwareConcurrency",
        "window-size=1280,1024"
    ]
    
    passed = True
    for check in checks:
        if check in script:
            print(f"✅ Found required flag/code: {check}")
        else:
            print(f"❌ Missing critical security feature: {check}")
            passed = False
            
    if passed:
        print("\n✅ ADA v2 Compliance Verified!")
    else:
        print("\n❌ Script failed security audit.")

if __name__ == "__main__":
    test_ridges_security()
