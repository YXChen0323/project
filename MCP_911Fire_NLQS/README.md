### Notion : https://www.notion.so/911-MCP-20eb7bf10bf880268b7adc15bd8be62e?source=copy_link

This directory hosts the assets for the 911Fire NLQS demo.

## MCP Client

`app/mcp_client.py` provides a small helper to communicate with Ollama's Model Context Protocol service.
`app/postgis_mcp_client.py` extends the client with PostGIS helpers.

Example usage:

```python
from mcp_client import MCPClient

client = MCPClient("http://localhost:11434")
ctx = client.create_context("demo", "system instructions")
response = client.generate(ctx["id"], "你好嗎？")
print(response["response"])
```
### PostGIS Example

```python
from postgis_mcp_client import PostGISMCPClient

pg_client = PostGISMCPClient(base_url="http://localhost:11434")
ctx = pg_client.create_geo_context(
    name="fire-calls",
    table="public.fire_calls",
    instructions="Describe the incidents",
    limit=10,
)
result = pg_client.generate(ctx["id"], "附近有幾個火警？")
print(result["response"])
```
