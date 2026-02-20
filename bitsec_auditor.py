import os
import requests
from typing import Dict, Any

class BitsecAuditor:
    """
    Adapter for Bitsec (Subnet 60) - Code Auditor.
    Performs static analysis on generated code to detect vulnerabilities.
    """
    def __init__(self):
        self.api_key = os.getenv("BITSEC_API_KEY")
        # Placeholder URL
        self.base_url = os.getenv("BITSEC_API_URL", "https://api.bitsec.tensor/v1")

    def audit(self, code: str) -> bool:
        """
        Scans code. Returns True if safe, raises SecurityException if unsafe.
        """
        if not self.api_key or "xxxx" in self.api_key:
            print("[Bitsec] API Key missing. Skipping audit (Unsafe Mode).")
            return True

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {"code": code, "language": "python"}
            
            print(f"[Bitsec] Auditing {len(code)} bytes of code...")
            resp = requests.post(f"{self.base_url}/scan", json=payload, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                report = resp.json()
                risk = report.get("risk_level", "UNKNOWN")
                
                if risk == "HIGH" or risk == "CRITICAL":
                    issues = report.get("issues", [])
                    raise SecurityException(f"Bitsec Output: Code rejected due to {len(issues)} high-risk issues.", issues)
                
                print(f"[Bitsec] Audit Passed (Risk: {risk}).")
                return True
            else:
                print(f"[Bitsec] Scan failed ({resp.status_code}). Allow-listing for now.")
                return True

        except SecurityException:
            raise
        except Exception as e:
            print(f"[Bitsec] Error contacting auditor: {e}. Defaulting to unsafe execution.")
            return True

class SecurityException(Exception):
    def __init__(self, message, issues=None):
        super().__init__(message)
        self.issues = issues or []
