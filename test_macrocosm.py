from brain import BrainRouter
from rich.console import Console

console = Console()

def test_macrocosm_integration():
    console.print("[bold white]🧪 Testing Macrocosm OS (SN25) Integration...[/bold white]")
    
    brain = BrainRouter()
    
    # Trigger Protein Folding
    console.print("\n[bold yellow] triggering 'Protein Folding' job...[/bold yellow]")
    result = brain.compute_heavy("PROTEIN_FOLDING", {"sequence": "MKTVR...LLV"})
    
    console.print("-" * 50)
    console.print(f"[bold green]Result:[/bold green] {result}")

    # Trigger Math Solver
    console.print("\n[bold yellow] triggering 'Math Solver' job...[/bold yellow]")
    result_math = brain.compute_heavy("MATH_SOLVER", {"equation": "42 * x = 1764"})
    
    console.print("-" * 50)
    console.print(f"[bold green]Result:[/bold green] {result_math}")

if __name__ == "__main__":
    test_macrocosm_integration()
