import subprocess
import json
import time
import os
from rich.console import Console

console = Console()

class BasilicaSandbox:
    """
    Wraps the Basilica CLI ('bs') to manage a remote sandbox for code execution.
    """
    def __init__(self, sandbox_name="openclaw-sandbox"):
        self.sandbox_name = sandbox_name
        # Try specific paths
        self.cli_paths = [
            os.path.expanduser("~/.basilica/bin/bs"),
            os.path.expanduser("~/.basilica/bin/basilica"),
            "/usr/local/bin/bs",
            "/usr/local/bin/basilica"
        ]

    def _run_cli(self, args):
        """Runs a Basilica CLI command and returns stdout."""
        cmd_exe = "bs" # Default reliance on PATH
        
        for p in self.cli_paths:
            if os.path.exists(p):
                cmd_exe = p
                break

        try:
            cmd = [cmd_exe] + args
            # print(f"Running: {' '.join(cmd)}") # Debug
                
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                env={**os.environ, "BASILICA_API_KEY": os.getenv("BASILICA_API_KEY", "")}
            )
            return result
        except Exception as e:
            return None

    def check_connection(self):
        """Checks if we can list resources (auth check)."""
        res = self._run_cli(["ls", "--json"])
        if res and res.returncode == 0:
            return True
        return False

    def get_sandbox_uid(self):
        """Finds the UID of the running sandbox deployment."""
        res = self._run_cli(["deploy", "ls", "--json"])
        if res and res.returncode == 0:
            try:
                data = json.loads(res.stdout)
                # It returns a dict like {"deployments": [], "total": 0}
                if isinstance(data, dict):
                    deployments = data.get("deployments", [])
                elif isinstance(data, list):
                    deployments = data
                else:
                    deployments = []
                    
                for dep in deployments:
                    # Check for name match
                    # Some versions might use 'name' or not show it in list directly but 'instanceName' is unique
                    # If we deployed with --name openclaw-test, does it show up?
                    # The example output doesn't show "name": "openclaw-test". It shows "public": true etc.
                    # Maybe it's not showing the name we gave it?
                    # Let's assume if there's only one deployment or if we just pick the first Active one for now?
                    # Or check if we can filter by name in CLI?
                    # The CLI usage says `bs deploy ls` lists all.
                    # The example output keys: instanceName, state, url, replicas, createdAt, public.
                    # It seems `name` is NOT in the output? That's annoying.
                    # But we only deploy one sandbox usually.
                    # Let's verify if we can match by name or if we should just take the Active one.
                    # Actually, we can use `bs deploy status <NAME>` maybe?
                    # Usage: `bs deploy status [aliases: get]`.
                    # Let's try `bs deploy get <NAME> --json` instead of ls?
                    
                    if dep.get("state") == "Active":
                         replicas = dep.get("replicas", {})
                         ready = replicas.get("ready", 0)
                         if ready > 0:
                             return dep.get("instanceName")
            except json.JSONDecodeError:
                pass
        return None

    def ensure_sandbox_running(self):
        """Ensures the sandbox deployment exists and is running."""
        uid = self.get_sandbox_uid()
        if uid:
            return uid
        
        # Create a temporary directory for the context or just use current with -f?
        # bs deploy doesn't seem to support -f for file?
        # Usage says [SOURCE]. If it's a directory, it looks for Dockerfile.
        # Let's rename Dockerfile.sandbox to Dockerfile temporarily or use a subdir?
        # Or just tell user to run from a dir?
        # Simplest: create a 'sandbox' dir
        sandbox_dir = os.path.join(os.getcwd(), "sandbox_build")
        os.makedirs(sandbox_dir, exist_ok=True)
        with open(os.path.join(sandbox_dir, "Dockerfile"), "w") as f:
            f.write("FROM python:3.9-slim\nCMD [\"sleep\", \"infinity\"]\n")

        res = self._run_cli([
            "deploy", 
            sandbox_dir,
            "--name", self.sandbox_name,
            "--cpu", "1",
            "--memory", "512Mi",
            "--detach",
            "--json"
        ])
        
        if res and res.returncode == 0:
            console.print("[green]🚀 Sandbox deployment initiated.[/green]")
            # Wait for it to be ready (naive wait)
            for _ in range(12): # Wait up to 60s
                time.sleep(5)
                uid = self.get_sandbox_uid()
                if uid:
                    console.print(f"[green]✅ Sandbox ready: {uid}[/green]")
                    return uid
                console.print("[dim]Waiting for sandbox...[/dim]")
        else:
            console.print(f"[red]❌ Failed to deploy sandbox:[/red] {res.stderr if res else 'Unknown error'}")
        
        return None

    def execute_code(self, code):
        """Executes Python code in the remote sandbox."""
        uid = self.get_sandbox_uid()
        if not uid:
             # Try to deploy if missing
            uid = self.ensure_sandbox_running()
            if not uid:
                return "Error: Sandbox not available."

        # Escape code for shell
        # We wrap it in safe execution
        # Note: 'bs exec' might behave differently than docker exec regarding quoting
        # Best to write to a file then run? 
        # bs exec doesn't easily support heredoc? 
        # Let's try simple python -c
        
        console.print(f"[dim]Executing in {uid}...[/dim]")
        # Escape quotes in code for the shell command
        safe_code = code.replace('"', '\\"').replace("'", "\\'")
        
        # bs exec <uid> -- python -c "..."
        res = self._run_cli(["exec", uid, "--", "python", "-c", code])
        
        if res and res.returncode == 0:
            return res.stdout
        else:
            return f"Error: {res.stderr if res else 'CLI execution failed'}"
