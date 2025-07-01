### Notion : https://www.notion.so/911-MCP-20eb7bf10bf880268b7adc15bd8be62e?source=copy_link

This directory hosts the assets for the 911Fire NLQS demo.

## MCP Client

`app/mcp_client.py` provides a small helper to communicate with Ollama's Model Context Protocol service.

Example usage:

```python
from mcp_client import MCPClient

client = MCPClient("http://localhost:11434")
ctx = client.create_context("demo", "system instructions")
response = client.generate(ctx["id"], "你好嗎？")
print(response["response"])
```
