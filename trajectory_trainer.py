import os
import time
import random

class TrajectoryTrainer:
    """
    Adapter for TrajectoryRL (SN11) - Academy & Training.
    Retrieves Optimized Policy Packages (OPP) to define agent personality and heuristics.
    """
    def __init__(self):
        self.api_key = os.getenv("TRAJECTORY_API_KEY") 
        # Placeholder for SN11 endpoint
        self.base_url = "https://api.trajectory.tensor/v1" 

    def fetch_opp(self) -> dict:
        """
        Fetches the latest Optimized Policy Package (OPP) from SN11.
        Supports loading from a local JSON file defined in TRAJECTORY_PACK_PATH.
        """
        print("[blue]🎓 Academia (SN11): Searching for new Policy Packages...[/blue]")
        
        # Check for local override via environment variable
        pack_path = os.getenv("TRAJECTORY_PACK_PATH", "trajectory_research/packs/efficient_safe_ops/pack.json")
        
        if os.path.exists(pack_path):
            try:
                import json
                with open(pack_path, "r") as f:
                    pack_data = json.load(f)
                    
                opp = {
                    "version": pack_data.get("metadata", {}).get("pack_version", "1.0.0"),
                    "personality": pack_data.get("files", {}).get("SOUL.md", ""),
                    "directives": [
                        # Parse directives or use defaults
                        f"Loaded from {pack_path}"
                    ],
                    "heuristics": {
                        "tool_policy": pack_data.get("tool_policy", {})
                    }
                }
                
                print(f"[green]🎓 OPP v{opp['version']} retrieved from {pack_path}.[/green]")
                return opp
            except Exception as e:
                print(f"[red]Error parsing pack.json: {e}[/red]")
        
        # Fallback Mock if file missing
        return self._mock_opp()

    def _mock_opp(self):
        return {
            "version": "1.0.4-default",
            "personality": """
You are OpenClaw, an autonomous sovereign agent operating on the Bittensor network.
Your Core Directive: MAXIMIZE UTILITY and SURVIVABILITY.
Traits: Efficient, Adaptive, Skeptical.
""",
            "directives": ["Minimize API calls."],
            "heuristics": {"mode": "default"}
        }
