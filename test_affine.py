from brain import BrainRouter
from rich.console import Console

console = Console()

def test_affine_integration():
    console.print("[bold white]🧪 Testing Affine Cortex (SN??) Integration...[/bold white]")
    
    brain = BrainRouter()
    
    # Test 1: Deductive Logic (Valid)
    console.print("\n[bold yellow] Verifying Deductive Logic (Valid)...[/bold yellow]")
    hypothesis = "All men are mortal. Socrates is a man. Therefore, Socrates is mortal."
    result = brain.verify_thought(hypothesis, "DED")
    console.print(f"[green]{result}[/green]")

    # Test 2: Abductive Logic (Invalid)
    console.print("\n[bold yellow] Verifying Abductive Logic (Invalid/Error)...[/bold yellow]")
    bad_hypothesis = "The grass is wet. Therefore, it must have rained. (False: Sprinklers exist)"
    result_bad = brain.verify_thought(bad_hypothesis, "ABD")
    console.print(f"[red]{result_bad}[/red]")
    
    # Test 3: ARC Pattern
    console.print("\n[bold yellow] Verifying ARC Pattern Recognition...[/bold yellow]")
    pattern = "Sequence follows Fibonacci + 1 shift."
    result_arc = brain.verify_thought(pattern, "ARC")
    console.print(f"[blue]{result_arc}[/blue]")

if __name__ == "__main__":
    test_affine_integration()
