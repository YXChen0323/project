import requests
from typing import Iterator, Optional, Dict, Any


class MCPClient:
    """Simple client for Ollama's Model Context Protocol (MCP).

    Parameters
    ----------
    base_url : str
        Base URL of the Ollama server (e.g. ``"http://localhost:11434"``).
    """

    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url.rstrip("/")

    # Context management -----------------------------------------------------
    def create_context(self, name: str, instructions: str) -> Dict[str, Any]:
        """Create a new MCP context."""
        payload = {"name": name, "instructions": instructions}
        resp = requests.post(f"{self.base_url}/api/mcp/context", json=payload)
        resp.raise_for_status()
        return resp.json()

    def update_context(self, context_id: str, instructions: str) -> Dict[str, Any]:
        """Update an existing MCP context."""
        payload = {"instructions": instructions}
        resp = requests.put(
            f"{self.base_url}/api/mcp/context/{context_id}", json=payload
        )
        resp.raise_for_status()
        return resp.json()

    def get_context(self, context_id: str) -> Dict[str, Any]:
        """Fetch a context's metadata."""
        resp = requests.get(f"{self.base_url}/api/mcp/context/{context_id}")
        resp.raise_for_status()
        return resp.json()

    def delete_context(self, context_id: str) -> None:
        """Delete an MCP context."""
        resp = requests.delete(f"{self.base_url}/api/mcp/context/{context_id}")
        resp.raise_for_status()

    # Generation -------------------------------------------------------------
    def generate(
        self,
        context_id: str,
        prompt: str,
        stream: bool = False,
    ) -> Iterator[str] | Dict[str, Any]:
        """Generate text using a specific MCP context."""
        payload = {
            "context": context_id,
            "prompt": prompt,
            "stream": stream,
        }
        resp = requests.post(
            f"{self.base_url}/api/mcp/generate", json=payload, stream=stream
        )
        resp.raise_for_status()
        if stream:
            for line in resp.iter_lines(decode_unicode=True):
                if line:
                    yield line
        else:
            return resp.json()
