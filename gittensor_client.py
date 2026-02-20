import json
import random
from pathlib import Path
from rich.console import Console

console = Console()

class GittensorClient:
    """
    Adapter for Gittensor (SN74) - The Contributor.
    Allows OpenClaw to identify and contribute to incentivized open-source repositories.
    """
    def __init__(self):
        # Path to the cloned repo weights
        self.weights_path = Path("gittensor_research/gittensor/validator/weights/master_repositories.json")
        self.repos = self._load_repos()

    def _load_repos(self) -> dict:
        """Loads the master repository list from the local file."""
        if not self.weights_path.exists():
            console.print(f"[red]Gittensor weights file not found at {self.weights_path}[/red]")
            return {}
        
        try:
            with open(self.weights_path, "r") as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[red]Error loading Gittensor repos: {e}[/red]")
            return {}

    def get_incentivized_repos(self, tier: str = None, limit: int = 10) -> list:
        """
        Returns a list of high-value repositories.
        """
        results = []
        for name, meta in self.repos.items():
            if tier and meta.get("tier") != tier:
                continue
            results.append({"name": name, **meta})
        
        # Sort by weight descending
        results.sort(key=lambda x: x.get("weight", 0), reverse=True)
        return results[:limit]

    def find_opportunity(self, repo_name: str = None) -> dict:
        """
        Simulates finding a contribution opportunity (Issue) in a target repo.
        """
        if not repo_name:
            # Pick a random high-value repo
            Gold_repos = self.get_incentivized_repos(tier="Gold", limit=50)
            if not Gold_repos:
                return {"error": "No Gold repositories available."}
            repo_name = random.choice(Gold_repos)["name"]

        console.print(f"[bold cyan]🔍 Gittensor: Scanning {repo_name} for issues...[/bold cyan]")
        
        # Mock Issue
        issue_id = random.randint(100, 5000)
        issue_types = ["Fix Memory Leak", "Add Unit Tests", "Refactor API", "Improve Documentation"]
        chosen_issue = random.choice(issue_types)
        
        return {
            "repo": repo_name,
            "issue_id": issue_id,
            "title": f"{chosen_issue} in core module",
            "description": "Please fix the identified issue found during static analysis.",
            "difficulty": "Hard"
        }

    def contribute(self, opportunity: dict, solution_code: str) -> str:
        """
        Simulates submitting a Pull Request (PR) to the repo.
        """
        repo = opportunity.get("repo")
        issue_id = opportunity.get("issue_id")
        
        console.print(f"[bold green]🚀 Gittensor: Contributing to {repo} (Issue #{issue_id})...[/bold green]")
        console.print(f"[dim]Code generated (len={len(solution_code)} chars). Submitting PR...[/dim]")
        
        # Mock PR
        pr_number = random.randint(5001, 9000)
        pr_url = f"https://github.com/{repo}/pull/{pr_number}"
        
        console.print(f"[bold white]✅ PR Submittted: {pr_url}[/bold white]")
        return pr_url
