# 🦞 Guia do Iniciante: OpenClaw Sovereign

Você já "ligou" a carcaça do robô. Agora precisamos dar a ele um cérebro funcionando.
Como você disse que é leigo, aqui está o passo a passo simplificado.

## Passo 1: O Combustível (API Keys)
Para o OpenClaw pensar, ele precisa de acesso a redes de inteligência (como se fosse crédito no celular).
No mundo do Bittensor, usamos "API Keys" para isso.

Você precisará conseguir essas chaves (códigos que começam com `sk-...`).
*Se você não tem chaves do Bittensor (Targon, Chutes), você pode usar chaves da OpenAI (ChatGPT) provisoriamente se alterarmos o código, mas o projeto original foca em Bittensor.*

## Passo 2: Configurar as Chaves
O arquivo `.env` é onde guardamos esses segredos.

1.  Abra o arquivo `.env` que está na pasta `/Users/TAO/gravity/agentao/` usando um editor de texto (Bloco de Notas, TextEdit, ou VS Code).
2.  Você verá linhas assim:
    ```bash
    TARGON_API_KEY=sk-tau-xxxxxxxxxxxxxxxxxxxxxxxx
    ```
3.  Apague o `sk-tau-xxxx...` e cole a **sua chave real** no lugar.
    *   Exemplo: `TARGON_API_KEY=sk-abc123456...`
4.  Faça isso para as chaves que você tiver. (Pelo menos `CHUTES_API_KEY` para o chat rápido).
5.  Salve o arquivo.

## Passo 3: Instalação Completa (Opcional por enquanto)
Nós fizemos uma instalação "leve". Se no futuro o robô reclamar que falta algo (`ModuleNotFoundError`), você precisará rodar aquele comando que demora:
`pip install -r requirements.txt`
(Mas deixe isso para depois se estiver funcionando).

## Passo 4: Conversar
Sempre que quiser usar:
1.  Abra o terminal.
2.  Digite:
    ```bash
    cd /Users/TAO/gravity/agentao
    python3 main.py --mode sovereign
    ```
3.  Converse!

---

**Dúvida comum:** "Onde eu consigo essas chaves `sk-tau` ou `sk-cht`?"
*Resposta:* Geralmente em sites como `taostats.io` ou através de validadores da rede Bittensor. Se você não tem acesso a isso, me avise, e podemos adaptar o robô para usar algo mais comum como a **OpenAI (ChatGPT)** ou **Anthropic (Claude)**.
