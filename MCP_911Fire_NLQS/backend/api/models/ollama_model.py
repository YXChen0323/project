import requests

OLLAMA_API_URL = "http://ollama_service:11434/api/generate"

def query_ollama_model(model_name: str, prompt: str):
    payload = {
        "model": "sqlcoder:7b",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    result = response.json()
    return result.get("response", "").strip()