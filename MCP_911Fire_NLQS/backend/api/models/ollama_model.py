import requests
import os

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama_service:11434/api/generate")

def query_ollama_model(model_name: str, prompt: str):
    payload = {
        "model": f"{model_name}",  # 假設所有模型使用 7b 版本，可根據實際調整
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        print(f"Ollama API 錯誤：{e}")
        return ""