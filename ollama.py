# ollama.py

import requests

class Ollama:
    def __init__(self, model):
        self.model = model

    def invoke(self, prompt):
        url = f"http://127.0.0.1:11434/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get('output', '')
        else:
            raise Exception(f"Erro ao executar o modelo: {response.text}")
