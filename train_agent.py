import os
import glob
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

def train_agent():
    console.print("[bold blue]🎓 TrajectoryRL (SN11) Agent Training Center[/bold blue]")
    console.print("Select a Policy Package (OPP) to train your agent:\n")
    
    # List examples
    example_path = "trajectory_research/packs/examples/*.json"
    files = glob.glob(example_path)
    
    if not files:
        console.print("[red]No training packs found in trajectory_research/packs/examples/[/red]")
        return
        
    table = Table(title="Available Policy Packages")
    table.add_column("ID", style="cyan")
    table.add_column("Pack Name", style="magenta")
    table.add_column("Description")
    
    choices = {}
    for i, fpath in enumerate(files):
        try:
            with open(fpath, "r") as f:
                data = json.load(f)
            name = data.get("metadata", {}).get("pack_name", "Unknown")
            desc = data.get("files", {}).get("AGENTS.md", "").split("\n")[0] # First line of AGENTS.md
            choices[str(i+1)] = fpath
            table.add_row(str(i+1), name, desc)
        except:
            continue
            
    console.print(table)
    
    selection = Prompt.ask("Select a Pack ID", choices=list(choices.keys()))
    selected_path = choices[selection]
    
    console.print(f"\n[yellow]Training agent with {selected_path}...[/yellow]")
    
    # 1. Update Env for Persistence (Optional, but good practice)
    # We won't modify .env to avoid messing up user config, 
    # but we will export it for this session's SoulManager
    os.environ["TRAJECTORY_PACK_PATH"] = selected_path
    
    # 2. Trigger Soul Update
    from soul_manager import SoulManager
    soul = SoulManager()
    success = soul.refresh_soul()
    
    if success:
        console.print(f"\n[bold green]✅ Training Complete![/bold green]")
        console.print("New Personality Loaded into [bold]SOUL.md[/bold].")
        console.print("The agent will now behave according to the selected policy.")
        
        # Preview
        with open("SOUL.md", "r") as f:
            console.print("\n[dim]" + f.read()[:300] + "...[/dim]")
    else:
        console.print("[bold red]❌ Training Failed.[/bold red]")

if __name__ == "__main__":
    train_agent()
