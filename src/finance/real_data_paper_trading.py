# ====================================================================
# NOME DO ARQUIVO: real_data_paper_trading.py
# LOCAL: Salvar na pasta src/finance/
# TEMA: Simulação de investimentos com Loop de Vigília (Sentinela)
# ====================================================================

import time
import requests
from datetime import datetime
import sys

class RealDataPaperTrading:
    """
    Simulador de Combate Avançado.
    O agente lê os preços REAIS do mercado via API e opera em Loop contínuo.
    """
    def __init__(self):
        self.log_file = "historico_de_trades_reais.txt"
        self.caixa_virtual = 10000.00 # $10.000 dólares imaginários
        print("\n🌐 [Oráculo] Conectando aos sensores de mercado global...")
        print(f"💰 [Caixa Virtual Inicial]: ${self.caixa_virtual:.2f}\n")

        self.crypto_ids = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "SOL": "solana"
        }

    def _get_real_price(self, asset: str) -> float:
        """Consulta a API pública da CoinGecko."""
        api_id = self.crypto_ids.get(asset)
        if not api_id:
            return 0.0

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={api_id}&vs_currencies=usd"
        
        try:
            resposta = requests.get(url, timeout=5)
            dados = resposta.json()
            return float(dados[api_id]["usd"])
        except Exception as e:
            print(f"    ❌ [Alerta] Falha de conexão com o Oráculo: {e}")
            return 0.0

    def execute_real_data_trade(self, asset: str, amount_usd: float):
        """O Agente lê o mercado real e anota no diário."""
        preco_atual = self._get_real_price(asset)
        
        if preco_atual == 0.0:
            print(f"    🛑 Oráculo cego para {asset}. Abortando.")
            return

        if amount_usd <= self.caixa_virtual:
            self.caixa_virtual -= amount_usd
            quantidade = amount_usd / preco_atual
            
            mensagem = (f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                        f"COMPRA | {asset} | "
                        f"Cotação: ${preco_atual} | Investido: ${amount_usd} | "
                        f"Qtd: {quantidade:.6f} | Caixa: ${self.caixa_virtual:.2f}\n")
            
            print(f"    ✅ Comprou {quantidade:.6f} {asset} a ${preco_atual}")
            
            with open(self.log_file, "a") as file:
                file.write(mensagem)
        else:
            print(f"    ❌ Sem saldo virtual para comprar {asset}.")

    def start_vigil_mode(self, interval_minutes: int):
        """
        O Loop Infinito. O agente acorda, opera e volta a dormir.
        """
        print(f"🦉 [Sentinela] Modo Vigília ativado. Operando a cada {interval_minutes} minuto(s).")
        print("⚠️ Pressione [Ctrl + C] no terminal a qualquer momento para abortar a missão.\n")
        
        ciclo = 1
        interval_seconds = interval_minutes * 60
        
        try:
            while True:
                print(f"--- 🔄 Iniciando Ciclo Operacional #{ciclo} ---")
                
                # A estratégia do agente neste ciclo:
                self.execute_real_data_trade("BTC", 100.00) # Compra $100 de BTC
                time.sleep(3) # Pausa para a API gratuita não bloquear
                self.execute_real_data_trade("ETH", 50.00)  # Compra $50 de ETH
                
                print(f"😴 [Sentinela] Ciclo {ciclo} concluído. Agente hibernando por {interval_minutes} minuto(s)...\n")
                
                ciclo += 1
                time.sleep(interval_seconds) # O script "congela" aqui até o tempo passar
                
        except KeyboardInterrupt:
            # Captura o momento em que você aperta Ctrl+C
            print("\n\n🛑 [Comando Manual] Sinal de interrupção recebido pelo Comandante.")
            print(f"💼 [Relatório Final] Caixa Virtual Restante: ${self.caixa_virtual:.2f}")
            print("🔌 Sistema Sentinela Desativado.")
            sys.exit(0)

# ==========================================
# EXECUTANDO A OPERAÇÃO EM LOOP
# ==========================================
if __name__ == "__main__":
    simulador = RealDataPaperTrading()
    
    # Inicia o loop. Coloquei 1 minuto para você ver funcionando rápido.
    # Depois você pode alterar para 60 (para rodar a cada 1 hora).
    simulador.start_vigil_mode(interval_minutes=1)
