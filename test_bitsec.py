from bitsec_auditor import BitsecAuditor, SecurityException
import os
from dotenv import load_dotenv

load_dotenv()

SAFE_CODE = """
def add(a, b):
    return a + b
"""

UNSAFE_CODE = """
import os
def hack():
    os.system("rm -rf /")
"""

def test_bitsec():
    print("Testing Bitsec (SN60) Auditor...")
    auditor = BitsecAuditor()
    
    print("\n--- Auditing Safe Code ---")
    try:
        if auditor.audit(SAFE_CODE):
            print("Safe code passed.")
    except SecurityException as e:
        print(f"Safe code wrongly rejected: {e}")

    print("\n--- Auditing Unsafe Code ---")
    try:
        if auditor.audit(UNSAFE_CODE):
            print("WARNING: Unsafe code passed (API might be in passthrough mode).")
    except SecurityException as e:
        print(f"Unsafe code correctly rejected: {e}")

if __name__ == "__main__":
    test_bitsec()
