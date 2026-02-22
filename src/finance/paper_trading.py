import time
import random
from datetime import datetime

class PaperTradingSimulator:
    """
    Simulador de Combate do OpenClaw.
    O agente analisa o mercado e anota as suas decisões num arquivo de log.
    Nenhum dinheiro real ou de teste é gasto aqui.
    """
    def __init__(self):
        self.log_file = "historico_de_trades_simulados.txt"
        self.caixa_virtual = 10000.00 # $10.000 dólares imaginários
        print("\n🟢 [Paper Trading] Simulador Inicializado. Risco Real: ZERO.")
        print(f"💰 [Caixa Virtual]: ${self.caixa_virtual:.2f}\n")

    def _get_mock_price(self, asset: str) -> float:
        """Simula a busca do preço de um ativo na Sub-rede 35."""
        precos_base = {"BTC": 85000.0, "ETH": 3200.0, "GOLD": 2400.0}
        base = precos_base.get(asset, 100.0)
        # Adiciona uma flutuação aleatória de -2% a +2%
        variacao = base * random.uniform(-0.02, 0.02)
        return round(base + variacao, 2)

    def execute_mock_trade(self, asset: str, amount_usd: float):
        """O Agente decide investir e anota no diário."""
        print(f"🤖 [OpenClaw] Analisando oportunidade em {asset}...")
        time.sleep(1) # Agente "pensando"
        
        preco_atual = self._get_mock_price(asset)
        
        # Lógica super simples: se ele tiver dinheiro, ele "compra"
        if amount_usd <= self.caixa_virtual:
            self.caixa_virtual -= amount_usd
            quantidade_comprada = amount_usd / preco_atual
            
            mensagem = (f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                        f"COMPRA SIMULADA | Ativo: {asset} | "
                        f"Preço: ${preco_atual} | Valor Investido: ${amount_usd} | "
                        f"Caixa Restante: ${self.caixa_virtual:.2f}\n")
            
            print(f"    ✅ Trade Aprovado! Comprado {quantidade_comprada:.4f} de {asset}.")
            
            # Escreve no arquivo de log (O diário do agente)
            with open(self.log_file, "a") as file:
                file.write(mensagem)
                
            print(f"    📝 Registro salvo em: {self.log_file}")
        else:
            print("    ❌ Saldo virtual insuficiente para esta manobra.")

# ==========================================
# EXECUTANDO A SIMULAÇÃO
# ==========================================
if __name__ == "__main__":
    simulador = PaperTradingSimulator()
    
    # O agente simula 3 operações diferentes
    simulador.execute_mock_trade("BTC", 1500.00)
    time.sleep(2)
    simulador.execute_mock_trade("ETH", 800.00)
    time.sleep(2)
    simulador.execute_mock_trade("GOLD", 2000.00)
    
    print(f"\n🏁 Simulação concluída. Verifique o arquivo '{simulador.log_file}'.")
