from brain import BrainRouter
from rich.console import Console

console = Console()

def test_gittensor_integration():
    console.print("[bold white]🧪 Testing Gittensor (SN74) Integration...[/bold white]")
    
    brain = BrainRouter()
    
    # Check if client loaded repos
    repo_count = len(brain.gittensor_client.repos)
    console.print(f"Loaded {repo_count} incentivized repositories from weights file.")
    
    if repo_count == 0:
        console.print("[red]FAILED: No repositories loaded.[/red]")
        return

    # Trigger contribution
    console.print("\n[bold yellow] triggering autonomous contribution...[/bold yellow]")
    result = brain.contribute_to_opensource()
    
    console.print("-" * 50)
    console.print(f"[bold green]Result:[/bold green] {result}")

if __name__ == "__main__":
    test_gittensor_integration()
