import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid

from api.router import route_task

app = FastAPI()

class JSONRPCRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict
    id: str

@app.post("/api/rpc")
async def handle_jsonrpc(request: Request):
    data = await request.json()
    try:
        rpc = JSONRPCRequest(**data)
        result = route_task(rpc.method, rpc.params)
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": rpc.id,
            "result": result
        })
    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": data.get("id", str(uuid.uuid4())),
            "error": {
                "code": -32600,
                "message": str(e)
            }
        }, status_code=500)