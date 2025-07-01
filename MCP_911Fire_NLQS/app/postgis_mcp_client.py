import psycopg2
import requests
from typing import Iterator, Dict, Any, List


class PostGISMCPClient:
    """Client integrating PostGIS queries with Ollama's Model Context Protocol.

    Parameters
    ----------
    dbname : str
        Name of the PostGIS database.
    user : str
        Database user name.
    password : str
        Password for the database user.
    host : str
        Hostname of the PostGIS server.
    port : str
        Port of the PostGIS server.
    base_url : str
        Base URL of the Ollama server (e.g. ``"http://localhost:11434"``).
    """

    def __init__(
        self,
        dbname: str = "mydatabase",
        user: str = "user",
        password: str = "123456",
        host: str = "postgres_service",
        port: str = "5432",
        base_url: str = "http://localhost:11434",
    ) -> None:
        self.db_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }
        self.base_url = base_url.rstrip("/")

    # ------------------------------------------------------------------
    # PostGIS helpers
    def _connect(self):
        return psycopg2.connect(**self.db_params)

    def fetch_geojson(self, table: str, geom_col: str = "geom", limit: int = 100) -> List[str]:
        """Return GeoJSON geometries from the specified table."""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            f"SELECT ST_AsGeoJSON({geom_col}) FROM {table} LIMIT %s", (limit,)
        )
        rows = cur.fetchall()
        conn.close()
        return [row[0] for row in rows]

    # ------------------------------------------------------------------
    # MCP wrappers
    def create_context(self, name: str, instructions: str) -> Dict[str, Any]:
        payload = {"name": name, "instructions": instructions}
        resp = requests.post(f"{self.base_url}/api/mcp/context", json=payload)
        resp.raise_for_status()
        return resp.json()

    def generate(
        self,
        context_id: str,
        prompt: str,
        stream: bool = False,
    ) -> Iterator[str] | Dict[str, Any]:
        payload = {"context": context_id, "prompt": prompt, "stream": stream}
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

    def create_geo_context(
        self,
        name: str,
        table: str,
        instructions: str,
        geom_col: str = "geom",
        limit: int = 100,
    ) -> Dict[str, Any]:
        """Create a context using GeoJSON data from a PostGIS table."""
        features = self.fetch_geojson(table, geom_col, limit)
        joined = "\n".join(features)
        full_instructions = f"{instructions}\n\nGeoJSON:\n{joined}"
        return self.create_context(name, full_instructions)
