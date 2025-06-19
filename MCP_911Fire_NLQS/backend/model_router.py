import os
import requests
from jsonrpc_util import wrap_jsonrpc, parse_jsonrpc_response

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

def call_llm_with_prompt(prompt: str, model: str = "phi3") -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        # 回傳純文字結果（SQL）
        return data["response"].strip()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"模型連線錯誤：{e}")
    except Exception as e:
        raise RuntimeError(f"模型回應處理錯誤：{e}")
