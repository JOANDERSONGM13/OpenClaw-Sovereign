import os
import json
import time
from rich.console import Console
from openai import Client
from stealth_browser import StealthBrowser
from bitsec_auditor import BitsecAuditor
from gopher_client import GopherClient

console = Console()

from handshake_consultant import HandshakeConsultant

from soul_manager import SoulManager

from context_loader import ContextLoader

from gittensor_client import GittensorClient

from macrocosm_client import MacrocosmClient

from affine_client import AffineClient

from taoshi_client import TaoshiClient
from src.tools.manako_vision import ManakoVision

class BrainRouter:
    """
    Decides between System 1 (Fast/Chutes) and System 2 (Deep/Targon) thinking
    using real Bittensor subnets via OpenAI-compatible endpoints.
    Also manages Body capabilities (RedTeam, Bitsec, Gopher, Handshake, Trajectory, Nexus).
    """
    def __init__(self):
        # 1. API Keys
        self.chutes_key = os.getenv("CHUTES_API_KEY")
        self.targon_key = os.getenv("TARGON_API_KEY")
        self.vanta_key = os.getenv("VANTA_API_KEY")
        
        # 2. Clients
        self.chutes_client = None
        self.targon_client = None
        self.vanta_client = None

        if self.chutes_key:
            self.chutes_client = Client(api_key=self.chutes_key, base_url="https://llm.chutes.ai/v1")
        
        if self.targon_key:
            self.targon_client = Client(api_key=self.targon_key, base_url="https://api.targon.com/v1")

        # 3. Subnet Modules
        self.stealth_browser = StealthBrowser()
        self.bitsec_auditor = BitsecAuditor()
        self.gopher_client = GopherClient()
        self.handshake_consultant = HandshakeConsultant()

        
        # v2.4 Modules
        self.soul_manager = SoulManager()
        self.system_prompt = self.soul_manager.load_soul()
        
        # v2.5 Modules (Data Layer)
        self.context_loader = ContextLoader()
        
        # v2.6 Modules (Contributor Layer)
        self.gittensor_client = GittensorClient()
        
        # v2.7 Modules (Compute Layer)
        self.macrocosm_client = MacrocosmClient()
        
        # v2.8 Modules (Verifier Layer)
        self.affine_client = AffineClient()
        
        # v2.9 Modules (Finance Layer)
        # v2.9 Modules (Finance Layer)
        self.taoshi_client = TaoshiClient()

        # v2.10 Modules (Vision Layer)
        self.manako_vision = ManakoVision()

    # ... existing methods ...

    # ... existing methods ...

    def _system_1_fast_response(self, prompt: str, is_sensitive: bool = False) -> str:
        """
        System 1: Fast, cheap, conversational. Use Chutes (SN64).
        If is_sensitive is True, requests a TEE (Trusted Execution Environment).
        """
        mode_label = "🔒 SECURE MODE (TEE)" if is_sensitive else "⚡ Fast Mode"
        console.print(f"[cyan]{mode_label} System 1 (Chutes SN64) activated...[/cyan]")
        
        if not self.chutes_client:
            return "[Mock] Chutes key missing. Response: " + prompt

        try:
            # Use configurable model or fallback to a known potentially valid one
            # Conceptual: In a real SDK, we would pass 'tier="tee"' or similar
            model_name = "chutes/kimi-k2.5-tee" if is_sensitive else os.getenv("CHUTES_MODEL", "chutes/nousresearch/hermes-3-llama-3.1-405b")
            
            response = self.chutes_client.chat.completions.create(
                model=model_name, 
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            console.print(f"[red]Error contacting Chutes: {e}[/red]")
            return f"[Fallback] Fast response to: {prompt}"

    def _system_2_deep_thought(self, prompt: str) -> str:
        """
        System 2: Deep, reasoning, strategic. Use Targon (SN4).
        Now augmented with Sovereign v2.5 Data Layer (Nexus).
        """
        console.print("[magenta]🧠 System 2 (Targon SN4) activated...[/magenta]")
        
        # Sovereign v2.5: Grounding Phase
        # Heuristic: Check if prompt needs deep context
        if "history" in prompt.lower() or "context" in prompt.lower() or "deep" in prompt.lower() or "research" in prompt.lower():
             # Basic topic extraction (first 50 chars or user cue)
             topic = prompt[:50]
             grounding_data = self.context_loader.get_deep_context(topic)
             # Augment the prompt with grounded truth
             prompt = f"Context from Data Universe (SN13/SN74):\n{grounding_data}\n\nUser Question:\n{prompt}"
        
        if not self.targon_client:
            return "[Mock] Targon key missing. Deep analysis of: " + prompt

        try:
            # Targon often requires specific parameters or models
            model_name = os.getenv("TARGON_MODEL", "deepseek-ai/DeepSeek-R1")
            
            response = self.targon_client.chat.completions.create(
                model=model_name, 
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=6000 # Deep thought needs tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            console.print(f"[red]Error contacting Targon ({e}). Falling back to System 1...[/red]")
            return self._system_1_fast_response(prompt)


    # ... existing methods ...

    def _system_3_cortex_thought(self, prompt: str) -> str:
        """
        System 3: Hyper-Logic, Critical Decision. Use Affine Cortex (SN120).
        The 'Supreme Judge' protocol.
        """
        console.print("[bold red]🧠 NEXUS SIGNAL: Activating Affine Cortex (SN120) - Protocolo do Arquiteto...[/bold red]")
        
        try:
            return self.affine_client.compute(prompt)
        except Exception as e:
            console.print(f"[red]Cortex Critical Failure: {e}. Fallback to System 2.[/red]")
            return self._system_2_deep_thought(prompt)

    def consult_specialist(self, query: str) -> str:
        """
        Routes query to Handshake58 (SN58) for expert advice.
        """
        return self.handshake_consultant.consult(query)

        self.chutes_key = os.getenv("CHUTES_API_KEY")
        self.targon_key = os.getenv("TARGON_API_KEY")
        
        # Initialize clients lazily to allow for missing keys during dev
        self.chutes_client = None
        self.targon_client = None

        # v2.2 Modules
        self.stealth_browser = StealthBrowser()
        self.bitsec_auditor = BitsecAuditor()
        self.gopher_client = GopherClient()
        
        if self.chutes_key:
            self.chutes_client = Client(
                api_key=self.chutes_key,
                base_url="https://llm.chutes.ai/v1" 
            )
        
        if self.targon_key:
            self.targon_client = Client(
                api_key=self.targon_key,
                base_url="https://api.targon.com/v1" 
            )

    def think(self, prompt: str, is_sensitive: bool = False) -> str:
        """
        Analyzes the prompt complexity and routes to the appropriate subnet.
        """
        if is_sensitive:
             console.print("[bold yellow]🔒 SECURE PROTOCOL: Forcing Chutes (SN64) TEE Enclave...[/bold yellow]")
             return self._system_1_fast_response(prompt, is_sensitive=True)

        complexity = self._evaluate_complexity(prompt)
        
        if complexity == "insane":
            return self._system_3_cortex_thought(prompt)
        elif complexity == "high":
            return self._system_2_deep_thought(prompt)
        else:
            return self._system_1_fast_response(prompt)

    def _evaluate_complexity(self, prompt: str) -> str:
        # Heuristic v2.6 (Cortex Edition)
        if "critical" in prompt.lower() or "architect" in prompt.lower() or "hyper" in prompt.lower() or "supreme" in prompt.lower():
            return "insane"
            
        if len(prompt) > 100:
            return "high"
            
        keywords = ["plan", "analyze", "analysis", "code", "context", "history", "research", "deep"]
        if any(k in prompt.lower() for k in keywords):
            return "high"
            
        return "low"




    def browse(self, url: str):
        """Uses RedTeam stealth browser to fetch content."""
        console.print(f"[green]🕵️ RedTeam Stealth Browsing: {url}...[/green]")
        try:
            return self.stealth_browser.browse(url)
        except Exception as e:
            console.print(f"[red]Browsing failed: {e}[/red]")
            return None

    def audit_code(self, code: str) -> bool:
        """Uses Bitsec to audit code safety."""
        console.print("[yellow]🛡️ Bitsec Auditing Code...[/yellow]")
        try:
            return self.bitsec_auditor.audit(code)
        except Exception as e:
            console.print(f"[bold red]AUDIT FAILED: {e}[/bold red]")
            return False

    def search_web(self, url: str) -> list:
        """Uses Gopher (SN42) to scrape and index a URL."""
        console.print(f"[blue]Gopher: Indexing {url}...[/blue]")
        try:
            return self.gopher_client.scrape(url)
        except Exception as e:
            console.print(f"[red]Gopher Search failed: {e}[/red]")
            return []

    def see(self, media_url: str, query: str = None) -> str:
        """
        Uses Manako (SN44) to analyze images or videos.
        """
        console.print(f"[magenta]👁️ Manako Vision: Analyzing {media_url}...[/magenta]")
        try:
            return self.manako_vision.look_at(media_url, query)
        except Exception as e:
            console.print(f"[red]Manako Vision failed: {e}[/red]")
            return "Vision analysis failed."

    def contribute_to_opensource(self, repo_name: str = None):
        """
        Uses Gittensor (SN74) to find an issue and propose a fix.
        """
        console.print("[cyan]🐙 Gittensor Agent: Searching for contribution opportunities...[/cyan]")
        try:
            opportunity = self.gittensor_client.find_opportunity(repo_name)
            if "error" in opportunity:
                return f"Gittensor Error: {opportunity['error']}"
            
            # Simulate Code Generation (using System 1/2 internally or just mock)
            # In production, this would feed 'opportunity' into Targon
            mock_fix = "def fix_bug():\n    pass # Implemented fix"
            
            pr_url = self.gittensor_client.contribute(opportunity, mock_fix)
            return f"Contribution successful! PR: {pr_url} (Repo: {opportunity['repo']})"
        except Exception as e:
            console.print(f"[red]Gittensor failed: {e}[/red]")
            return "Contribution failed."

    def compute_heavy(self, task_type: str, payload: dict) -> str:
        """
        Offloads heavy computation to Macrocosm OS (SN25).
        """
        console.print(f"[magenta]🌌 Macrocosm Agent: Requesting Heavy Compute for {task_type}...[/magenta]")
        try:
            job_id = self.macrocosm_client.dispatch_job(task_type, payload)
            
            # Simulate waiting for result
            console.print(f"[dim]Waiting for distributed completion (Job {job_id})...[/dim]")
            time.sleep(2.5) 
            
            result = self.macrocosm_client.check_status(job_id)
            if result.get("status") == "COMPLETED":
                return f"Compute Job {job_id} Completed: {result.get('result')}"
            else:
                return f"Job {job_id} is still PROCESSING."
        except Exception as e:
            console.print(f"[red]Macrocosm Compute failed: {e}[/red]")
            return "Compute task failed."

    def verify_thought(self, thought: str, task_type: str = "DED") -> str:
        """
        Verifies reasoning using Affine Cortex (SN??).
        Example task_types: DED (Deduction), ABD (Abduction), ARC (Pattern).
        """
        console.print(f"[magenta]🧠 Affine Cortex: Verifying thought in {task_type} environment...[/magenta]")
        try:
            result = self.affine_client.verify_thought(thought, task_type)
            
            if "error" in result:
                return f"Affine Error: {result['error']}"
            
            status = "VALID" if result.get("valid") else "INVALID"
            score = result.get("score", 0.0)
            feedback = result.get("feedback", "No feedback.")
            
            return f"Verification Result ({status}): Score {score:.2f}. Feedback: {feedback}"
        except Exception as e:
            console.print(f"[red]Affine Verification failed: {e}[/red]")
            return "Verification failed."

    def get_market_sentiment(self, limit=10) -> list:
        """
        Retrieves latest financial signals from Vanta Network (SN).
        Reads from shared 'vanta_signals.json' produced by vanta_observer.py.
        """
        signal_file = "vanta_signals.json"
        if not os.path.exists(signal_file):
            return ["No active market signals found. Is vanta_observer running?"]
        
        try:
            with open(signal_file, "r") as f:
                signals = json.load(f)
            
            # Format signals for the brain
            summary = []
            for s in signals[-limit:]:
                summary.append(f"[{s['timestamp']}] {s['miner_hotkey'][:5]}.. traded {s['trade_pair']} ({s['order_type']} x{s['leverage']}) @ {s['price']}")
            
            return summary
        except Exception as e:
            console.print(f"[red]Error reading Vanta signals: {e}[/red]")
            return []
