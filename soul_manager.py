import os
import json
from trajectory_trainer import TrajectoryTrainer

class SoulManager:
    """
    Manages the Agent's "Soul" (Personality and Directives).
    Intefaces with TrajectoryRL (SN11) to optimize behavior over time.
    """
    def __init__(self, soul_path="SOUL.md"):
        self.soul_path = soul_path
        self.trainer = TrajectoryTrainer()

    def refresh_soul(self):
        """
        Fetches the latest Optimized Policy Package (OPP) from SN11 and updates SOUL.md.
        """
        try:
            opp = self.trainer.fetch_opp()
            self._write_soul(opp)
            return True
        except Exception as e:
            print(f"[red]Failed to refresh soul: {e}[/red]")
            return False

    def load_soul(self) -> str:
        """
        Reads the current SOUL.md content to be used as system prompt.
        If file doesn't exist, fetching a new one first.
        """
        if not os.path.exists(self.soul_path):
            print("[yellow]SOUL.md not found. Initializing from Academy (SN11)...[/yellow]")
            self.refresh_soul()
        
        try:
            with open(self.soul_path, "r") as f:
                return f.read()
        except:
            return "You are a default AI assistant."

    def _write_soul(self, opp: dict):
        """
        Writes the OPP dictionary to SOUL.md in a readable markdown format.
        """
        content = f"""# Agent Soul v{opp.get('version', '1.0')}
        
## Personality
{opp.get('personality', '')}

## Directives
"""
        for directive in opp.get('directives', []):
            content += f"- {directive}\n"
            
        content += "\n## Operational Heuristics\n"
        for key, value in opp.get('heuristics', {}).items():
            content += f"- **{key}**: {value}\n"
            
        with open(self.soul_path, "w") as f:
            f.write(content)
        print(f"[green]Soul updated/written to {self.soul_path}[/green]")
