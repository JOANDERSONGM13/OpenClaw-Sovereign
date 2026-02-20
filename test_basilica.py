from basilica_sandbox import BasilicaSandbox
import sys

def main():
    print("Initializing BasilicaSandbox...")
    sandbox = BasilicaSandbox()
    
    print("\n1. Checking Auth/Connection...")
    if sandbox.check_connection():
        print("✅ Connection Successful!")
    else:
        print("❌ Connection Failed. Please ensure you have run 'bs login'.")
        sys.exit(1)

    print("\n2. Deploying/Finding Sandbox 'openclaw-test'...")
    uid = sandbox.ensure_sandbox_running()
    
    if uid:
        print(f"✅ Sandbox Active. UID: {uid}")
        
        print("\n3. Executing Remote Code...")
        code = "print('Hello from Basilica Subnet 39! 🏰')"
        output = sandbox.execute_code(code)
        
        print(f"\n--- Output ---\n{output}\n--------------")
        
        if "Hello" in output:
            print("✅ Remote Execution Confirmed!")
        else:
            print("⚠️ Unexpected output.")
            
    else:
        print("❌ Failed to deploy sandbox.")

if __name__ == "__main__":
    main()
