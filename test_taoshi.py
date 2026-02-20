from taoshi_client import TaoshiClient
from rich.console import Console

console = Console()

def test_hwm_payouts():
    console.print("[bold white]🧪 Testing Taoshi (SN8) HWM Logic...[/bold white]")
    
    client = TaoshiClient()
    
    # 1. Initial State (Balance 100, HWM 100)
    console.print("\n[cyan]Step 1: Check Initial State[/cyan]")
    # Should fail payout (Balance == HWM)
    result = client.request_payout(10.0)
    assert result == False, "Payout should be denied at HWM"
    
    # 2. Profitable Trade (+20 TAO) -> Balance 120
    console.print("\n[cyan]Step 2: Record Profit (+20 TAO)[/cyan]")
    client.record_trade(20.0)
    # HWM might update here depending on implementation, 
    # but usually HWM updates on performance fee realization.
    # In my simplified implementation, HWM updates on record_trade if it exceeds previous HWM.
    # Let's check logic:
    # "Adding the requirement of beating the prior HWM value on realized returns in order to recieve payouts"
    # Actually, if I update HWM immediately, then Balance == HWM, and Payout is denied again?
    # Ah, standard HWM:
    # HWM is the HIGH WATERMARK. If Balance > HWM, you can take a fee on (Balance - HWM). 
    # AND THEN HWM updates to Balance.
    
    # Let me re-read my `taoshi_client.py` implementation logic.
    # self.high_watermark = self.current_balance (if > old HWM)
    # self.request_payout: Checks if Balance > HWM.
    
    # 3. Payout 10 TAO (Allowed, since 120 > 100)
    console.print("\n[cyan]Step 3: Request Payout (10 TAO)[/cyan]")
    result = client.request_payout(10.0)
    assert result == True, "Payout should be approved (120 > 100)"
    
    # 4. Attempt Payout > Profit (e.g., 20 TAO, but balance is 110, HWM 100. Profit=10)
    console.print("\n[cyan]Step 4: Request Excess Payout (20 TAO)[/cyan]")
    result = client.request_payout(20.0)
    assert result == False, "Payout should be denied (Request > Available Profit)"
    
    # 5. Losing Trade (-15 TAO) -> Balance 95 (Below HWM 100)
    console.print("\n[cyan]Step 5: Record Loss (-15 TAO)[/cyan]")
    client.record_trade(-15.0)
    
    # 6. Attempt Payout
    console.print("\n[cyan]Step 6: Request Payout (5 TAO)[/cyan]")
    result = client.request_payout(5.0)
    assert result == False, "Payout should be denied (Balance < HWM)"
    
    console.print("\n[bold green]✅ HWM Logic Verified![/bold green]")

if __name__ == "__main__":
    # Reset Ledger for test
    import os
    if os.path.exists("taoshi_ledger.json"):
        os.remove("taoshi_ledger.json")
    test_hwm_payouts()
