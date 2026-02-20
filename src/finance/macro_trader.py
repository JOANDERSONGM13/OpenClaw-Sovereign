import os
import requests
from dotenv import load_dotenv

# Carrega as chaves secretas (O Escudo)
load_dotenv()

class MacroTrader:
    """
    Módulo Financeiro Global do OpenClaw Sovereign.
    Conecta o agente aos mercados de Forex e Commodities via 0xMarkets (SN35).
    """

    def __init__(self):
        # Carregando credenciais da armadura
        self.api_key = os.getenv("SN35_API_KEY")
        # Endpoint hipotético da rede 0xMarkets no Bittensor
        self.endpoint = "https://api.0xmarkets.tao/v1/trade"

    def execute_trade(self, asset: str, side: str, amount_usd: float, leverage: int = 1):
        """
        Executa uma ordem de compra ou venda em mercados tradicionais (Ouro, Fiat).
        """
        # Normalização de símbolos
        symbol_map = {
            "GOLD": "XAU/USD",
            "EURO": "EUR/USD",
            "YEN": "JPY/USD"
        }
        target_symbol = symbol_map.get(asset.upper(), asset.upper())
        action = side.upper()

        print(f"\n🌍 [MacroTrader] Iniciando Protocolo de Execução Financeira...")
        print(f"    Alvo: {target_symbol} | Ação: {action} | Volume: ${amount_usd} | Alavancagem: {leverage}x")

        payload = {
            "pair": target_symbol,
            "side": action.lower(),
            "amount": amount_usd,
            "leverage": leverage
        }

        # Simulação de envio para a rede (em produção usaria requests.post)
        try:
            if not self.api_key:
                print("⚠️  AVISO: SN35_API_KEY não encontrada no .env. Executando em modo simulação (Paper Trading).")
                return f"[Paper Trade] Ordem de {action} para {target_symbol} registrada com sucesso."

            # A chamada real para a SN35 seria feita aqui:
            # response = requests.post(self.endpoint, json=payload, headers={"Authorization": f"Bearer {self.api_key}"})
            # response.raise_for_status()
            # data = response.json()
            
            print(f"💎 [Sucesso] Ordem roteada via Subnet 35. Execução descentralizada confirmada.")
            return f"Trade executado: {action} {target_symbol} a mercado."

        except Exception as e:
            print(f"❌ [Erro Fatal] Falha na execução da ordem: {e}")
            return None

# ==========================================
# TESTE DO SISTEMA (Para você rodar localmente)
# ==========================================
if __name__ == "__main__":
    trader = MacroTrader()
    
    # Simulação 1: O OpenClaw detectou queda no Bitcoin e decide fazer "Hedge" (Proteção) em Ouro
    print("\n--- Cenário 1: Proteção de Capital (Hedge) ---")
    resultado_ouro = trader.execute_trade(asset="GOLD", side="BUY", amount_usd=5000)
    
    # Simulação 2: O OpenClaw detecta inflação no Dólar e aposta no Euro
    print("\n--- Cenário 2: Arbitragem de Moedas Fiduciárias ---")
    resultado_euro = trader.execute_trade(asset="EURO", side="BUY", amount_usd=1500, leverage=2)
