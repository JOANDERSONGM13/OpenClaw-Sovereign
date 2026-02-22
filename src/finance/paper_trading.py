# ====================================================================
# NOME DO ARQUIVO: paper_trading.py
# LOCAL: Salvar na pasta src/finance/
# TEMA: Simulação de Combate com Loop de Vigília e Realização de Lucro (Take Profit)
# ====================================================================

import time
import requests
from datetime import datetime
import sys

class RealDataPaperTrading:
    """
    Simulador de Combate Definitivo.
    O agente opera em Loop, compra na baixa e VENDE automaticamente ao atingir a meta de lucro.
    """
    def __init__(self):
        self.log_file = "historico_de_trades_reais.txt"
        self.caixa_virtual = 10000.00
        self.meta_lucro = 1.05  # Meta de 5% de lucro para vender (Take Profit)
        
        # O Agente agora tem uma "Mochila" para guardar o que comprou
        self.portfolio = {
            "BTC": {"quantidade": 0.0, "total_gasto": 0.0},
            "ETH": {"quantidade": 0.0, "total_gasto": 0.0},
            "SOL": {"quantidade": 0.0, "total_gasto": 0.0}
        }
        
        print("\n🌐 [Oráculo] Sensores de mercado online.")
        print(f"💰 [Caixa Virtual]: ${self.caixa_virtual:.2f}")
        print(f"🎯 [Estratégia]: Vender automaticamente com {(self.meta_lucro - 1) * 100}% de lucro.\n")

        self.crypto_ids = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana"}

    def _get_real_price(self, asset: str) -> float:
        """Consulta a API pública da CoinGecko."""
        api_id = self.crypto_ids.get(asset)
        if not api_id: return 0.0
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={api_id}&vs_currencies=usd"
        try:
            resposta = requests.get(url, timeout=5)
            return float(resposta.json()[api_id]["usd"])
        except Exception:
            return 0.0

    def evaluate_and_trade(self, asset: str, amount_usd_to_buy: float):
        """Lógica do Agente: Avalia se deve VENDER o que tem, ou COMPRAR mais."""
        preco_atual = self._get_real_price(asset)
        if preco_atual == 0.0: return
        
        # 1. VERIFICA SE TEMOS LUCRO PARA VENDER (TAKE PROFIT)
        inventario = self.portfolio[asset]
        if inventario["quantidade"] > 0:
            preco_medio_pago = inventario["total_gasto"] / inventario["quantidade"]
            
            # Se o preço atual for 5% maior que o preço médio que pagamos...
            if preco_atual >= (preco_medio_pago * self.meta_lucro):
                valor_venda = inventario["quantidade"] * preco_atual
                lucro_liquido = valor_venda - inventario["total_gasto"]
                
                # Executa a Venda
                self.caixa_virtual += valor_venda
                mensagem = (f"[{datetime.now().strftime('%H:%M:%S')}] 🟢 VENDA (LUCRO) | {asset} | "
                            f"Preço: ${preco_atual} | Lucro: +${lucro_liquido:.2f} | Caixa: ${self.caixa_virtual:.2f}\n")
                
                print(f"    🤑 [TAKE PROFIT] Vendeu {asset} com lucro de ${lucro_liquido:.2f}!")
                
                # Zera a mochila deste ativo
                self.portfolio[asset] = {"quantidade": 0.0, "total_gasto": 0.0}
                
                with open(self.log_file, "a") as file:
                    file.write(mensagem)
                return # Encerra o turno deste ativo, já vendemos.

        # 2. SE NÃO VENDEU, TENTA COMPRAR MAIS (ACUMULAÇÃO)
        if amount_usd_to_buy <= self.caixa_virtual:
            self.caixa_virtual -= amount_usd_to_buy
            qtd_comprada = amount_usd_to_buy / preco_atual
            
            # Guarda na mochila
            self.portfolio[asset]["quantidade"] += qtd_comprada
            self.portfolio[asset]["total_gasto"] += amount_usd_to_buy
            
            mensagem = (f"[{datetime.now().strftime('%H:%M:%S')}] 🔴 COMPRA | {asset} | "
                        f"Preço: ${preco_atual} | Investido: ${amount_usd_to_buy} | Caixa: ${self.caixa_virtual:.2f}\n")
            
            print(f"    🛒 Comprou {qtd_comprada:.6f} {asset} a ${preco_atual}")
            
            with open(self.log_file, "a") as file:
                file.write(mensagem)
        else:
            print(f"    ❌ Sem saldo para comprar {asset}. Aguardando vendas para fazer caixa.")

    def start_vigil_mode(self, interval_minutes: int):
        print(f"🦉 [Sentinela] Modo Vigília ativado. Loop de {interval_minutes} minuto(s). [Ctrl+C] para sair.\n")
        ciclo = 1
        interval_seconds = interval_minutes * 60
        try:
            while True:
                print(f"--- 🔄 Ciclo Operacional #{ciclo} ---")
                self.evaluate_and_trade("BTC", 100.00) 
                time.sleep(3) 
                self.evaluate_and_trade("ETH", 50.00)  
                
                print(f"😴 Fim do Ciclo {ciclo}. Hibernando...\n")
                ciclo += 1
                time.sleep(interval_seconds) 
        except KeyboardInterrupt:
            print("\n🛑 Sistema Desativado pelo Comandante.")
            print(f"💼 Caixa Final: ${self.caixa_virtual:.2f}")
            sys.exit(0)

if __name__ == "__main__":
    simulador = RealDataPaperTrading()
    simulador.start_vigil_mode(interval_minutes=1)
