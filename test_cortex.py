from brain import BrainRouter
from rich.console import Console

console = Console()

def test_cortex_edition():
    console.print("[bold white]🧪 Testing Cortex Edition v2.6 (Subnet 120)...[/bold white]")
    
    brain = BrainRouter()
    
    # Level 1: Reflex
    console.print("\n[cyan]Target: Level 1 (Reflex)[/cyan]")
    brain.think("Hi there!")
    
    # Level 2: Reasoning
    console.print("\n[magenta]Target: Level 2 (Reasoning)[/magenta]")
    brain.think("Plan a marketing strategy for a new coffee brand.")
    
    # Level 3: Hyper-Logic (The Architect)
    console.print("\n[red]Target: Level 3 (Hyper-Logic - The Architect)[/red]")
    prompt = "CRITICAL: Design a supreme architecture for a planetary governance AI using game theory."
    result = brain.think(prompt)
    
    print("\nResult from Architect:")
    print(result)

if __name__ == "__main__":
    test_cortex_edition()
