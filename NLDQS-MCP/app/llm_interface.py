import requests

def query_llm(prompt: str) -> str:
    response = requests.post(
        "http://ollama_service:11434/api/generate",
        json={
            "model": "llama3.2:latest",
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    return response.json()["response"].strip()
