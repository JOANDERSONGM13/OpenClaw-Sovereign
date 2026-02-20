import json
import os
from pathlib import Path
from rich.console import Console

console = Console()

class TaoshiClient:
    """
    Adapter for Taoshi (SN8) - Financial Management & Proprietary Trading.
    Implements High Watermark (HWM) logic for payouts.
    """
    def __init__(self):
        self.ledger_file = Path("taoshi_ledger.json")
        self.current_balance = 100.0  # Initial Capital (TAO)
        self.high_watermark = 100.0   # Initial HWM
        self._load_ledger()

    def _load_ledger(self):
        if self.ledger_file.exists():
            try:
                with open(self.ledger_file, "r") as f:
                    data = json.load(f)
                    self.current_balance = data.get("balance", 100.0)
                    self.high_watermark = data.get("hwm", 100.0)
            except Exception as e:
                console.print(f"[red]Error loading ledger: {e}[/red]")

    def _save_ledger(self):
        with open(self.ledger_file, "w") as f:
            json.dump({
                "balance": self.current_balance,
                "hwm": self.high_watermark
            }, f, indent=4)

    def record_trade(self, profit_loss: float):
        """
        Record a trade result (profit or loss).
        """
        self.current_balance += profit_loss
        console.print(f"[cyan]Trade Recorded: {profit_loss:+.2f} TAO. New Balance: {self.current_balance:.2f} TAO[/cyan]")
        
        # Check if HWM is breached (only on realized gains)
        if self.current_balance > self.high_watermark:
            console.print(f"[green]🌊 New Peak Equity: {self.current_balance:.2f} (HWM: {self.high_watermark:.2f})[/green]")
            # We do NOT update HWM here. HWM is the threshold for payouts.
            # We only update HWM *after* a payout resets the watermark 
            # OR if we want to track "Peak Equity" separately.
            
            # Correction: In many systems, HWM tracks peak equity.
            # BUT Payouts are allowed from (Current - HWM).
            # If we update HWM to Current immediately, (Current - HWM) = 0.
            # So we must NOT update HWM until the payout is processed or the period ends?
            
            # Implementation Strategy: 
            # 1. high_watermark = The historical peak value *before* current un-withdrawn profits.
            # Actually, let's keep it simple:
            # HWM raises ONLY when we confirm a new higher baseline.
            # For a trading bot, "payout" means taking profit off the table.
            # If we take profit, the Balance drops. The HWM should stay at the high point?
            # Example: Start 100. Profit +20 -> Balance 120. HWM 100.
            # Payout 10. Balance 110. HWM 100? Or HWM 110?
            
            # User Input: "Adding the requirement of beating the prior HWM value on realized returns in order to recieve payouts"
            # This implies: Payout Condition: Realized Return > HWM.
            # Realized Return usually means closed trades.
            pass # We don't auto-update HWM here for the sake of payout logic.
        
        self._save_ledger()

    def request_payout(self, amount: float) -> bool:
        """
        Request a payout. 
        Constraint: Can only pay out if current_balance > high_watermark.
        """
        if self.current_balance <= self.high_watermark:
             console.print(f"[red]🚫 Payout Denied: High Watermark ({self.high_watermark:.2f}) not beaten. Current: {self.current_balance:.2f}[/red]")
             return False
             
        available_profit = self.current_balance - self.high_watermark
        
        if amount > available_profit:
            console.print(f"[red]🚫 Payout Denied: Request {amount:.2f} exceeds available profit ({available_profit:.2f}) above HWM.[/red]")
            return False
            
        self.current_balance -= amount
        
        # After payout, do we raise the HWM? 
        # Scenario: 
        # 1. Start 100. Trade +50 -> 150. HWM 100.
        # 2. Payout 20. Balance 130. 
        # 3. New Trade -40 -> 90.
        # If HWM stays 100, we can still pay out 30? No, balance 90 < 100.
        
        # If we payout, we usually consider that profit "realized and gone".
        # So we should probably raise HWM to reflect that we've "banked" that level?
        # Actually, if we payout, the "water level" drops.
        # But HWM prevents paying out *principal* or *previous peaks*.
        
        # Let's say HWM tracks the "Capital Base + Reinvested Profit".
        # If we withdraw, we don't necessarily change HWM, we just reduce Balance.
        # But if we treat HWM as "Highest Value Ever Reached", then 150 was the HWM. 
        # If we withdraw 20, Balance 130. We shouldn't pay again until we beat 150?
        # That would mean we can't withdraw the remaining 30 profit? That seems wrong for a "Dividend".
        
        # Interpretation: HWM = 100. Balance = 150.
        # We can withdraw 50.
        # If we withdraw 20, Balance = 130. Remaining withdrawable = 30.
        # HWM stays 100.
        
        console.print(f"[green]💸 Payout Approved: {amount:.2f} TAO. New Balance: {self.current_balance:.2f}[/green]")
        self._save_ledger()
        return True

    def get_status(self):
        return {
            "balance": self.current_balance,
            "hwm": self.high_watermark,
            "can_payout": self.current_balance > self.high_watermark
        }
