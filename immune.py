import hashlib
import json
import os
from typing import Optional
from rich.console import Console
from basilica_sandbox import BasilicaSandbox

console = Console()

class ImmuneSystem:
    """
    Verifies code signatures and executes code safely within a Basilica (Subnet 39) sandbox.
    """
    def __init__(self):
        self.console = Console()
        self.trusted_skills_path = os.getenv("TRUSTED_SKILLS_PATH", "./trusted_skills.json")
        self.sandbox = BasilicaSandbox()
        self._load_trusted_skills()
        self._check_basilica()

    def _load_trusted_skills(self):
        try:
            with open(self.trusted_skills_path, 'r') as f:
                self.trusted_data = json.load(f)
                self.trusted_hashes = set(self.trusted_data.get("trusted_hashes", []))
                for tool in self.trusted_data.get("whitelisted_tools", []):
                    if "hash" in tool:
                        self.trusted_hashes.add(tool["hash"])
        except FileNotFoundError:
            self.trusted_hashes = set()
            self.console.print(f"[yellow]Warning: Trusted skills file not found at {self.trusted_skills_path}[/yellow]")

    def _check_basilica(self):
        if self.sandbox.check_connection():
            self.console.print("[green]🏛️  Basilica (Subnet 39) Connected.[/green]")
        else:
            self.console.print("[yellow]⚠️ Basilica not connected. Check BASILICA_API_KEY in .env[/yellow]")

    def scan_code(self, code: str) -> bool:
        """
        Scans code for malicious patterns and checks against trusted hashes.
        """
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        
        # 1. Check Whitelist
        if code_hash in self.trusted_hashes:
            self.console.print(f"[green]✅ Code hash verified: {code_hash[:8]}...[/green]")
            return True

        # 2. Static Analysis (Basic)
        dangerous_terms = ["os.system", "subprocess", "shutil.rmtree", "eval(", "exec("]
        for term in dangerous_terms:
            if term in code:
                self.console.print(f"[bold red]🚫 BLOCKED: Dangerous term '{term}' detected![/bold red]")
                return False

        self.console.print(f"[yellow]⚠️ Code hash unknown: {code_hash[:8]}... Proceeding with caution using Remote Sandbox.[/yellow]")
        return True

    def execute_safely(self, code: str):
        """
        Sends code to Basilica Sandbox for remote execution.
        """
        self.console.print("[bold green]🔒 Sending to Basilica Sandbox...[/bold green]")
        output = self.sandbox.execute_code(code)
        self.console.print(f"[dim]Output:[/dim]\n{output}")

