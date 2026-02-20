import os
import requests

class ManakoVision:
    def __init__(self):
        # Novo Endpoint do Manako (Hipotético)
        self.endpoint = "https://api.manako.tao/v1/visual-search"
        self.api_key = os.getenv("MANAKO_API_KEY")

    def look_at(self, media_url: str, query: str = None):
        """
        Usa a SN44 para descrever uma imagem ou encontrar algo num vídeo.
        """
        print(f"[*] Nexus Signal: Ativando Olho Manako (SN44) para: {media_url}...")
        
        payload = {"url": media_url}
        if query:
            payload["query"] = query # Ex: "Encontre o momento do gol" ou "Descreva a roupa"
            mode = "video_search"
        else:
            mode = "image_captioning"

        try:
            response = requests.post(
                f"{self.endpoint}/{mode}",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            data = response.json()
            
            # O Manako devolve a descrição ou o timestamp
            return f"👁️ Visão Manako: {data.get('description', data.get('timestamp'))}"

        except Exception as e:
            return f"Erro Visual: {e}"
