from rich.console import Console
from data_universe import Subnet13Client
from clean_data import Subnet74Client

console = Console()

class ContextLoader:
    """
    The Nexus: Orchestrates the Data & Context Layer (v2.5).
    Connects Memory (SN13) to Filter (SN74) to Grounding.
    """
    def __init__(self):
        self.sn13 = Subnet13Client() # Data Universe
        self.sn74 = Subnet74Client() # Clean Data

    def get_deep_context(self, topic: str):
        """
        Retrieves, cleans, and structures deep context for a given topic.
        Target: Zero Hallucination.
        """
        console.print(f"[bold magenta]🔮 Nexus Signal: Mining Data Universe (SN13) for '{topic}'...[/bold magenta]")
        
        # 1. Coleta Massiva (Raw Data)
        raw_data = self.sn13.fetch_bulk(topic, limit=1000)
        
        if not raw_data:
            return "No historical data found."

        console.print(f"[bold cyan]🔮 Nexus Signal: Refining data with Quality Filter (SN74)...[/bold cyan]")
        
        # 2. Refinamento (Cleaning)
        clean_context = self.sn74.process(raw_data)
        
        return clean_context
