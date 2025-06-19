import uuid

def wrap_jsonrpc(method: str, params: dict, request_id: str = None):
    return {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id or str(uuid.uuid4())
    }

def parse_jsonrpc_response(response: dict):
    if response.get("error"):
        raise Exception(f"Model Error: {response['error']}")
    return response.get("result")
