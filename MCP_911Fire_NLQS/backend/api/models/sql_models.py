from .ollama_model import query_ollama_model

def query(model_name: str, prompt: str, params=None):
    response_text = query_ollama_model(model_name, prompt)
    sql = extract_sql(response_text)
    summary = summarize_sql(sql, params)
    return {"sql": sql, "summary": summary}

def extract_sql(text: str):
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if line.lower().startswith("select"):
            if "count" in line.lower() and "query_anything.emergency_calls" in line.lower():
                return line
            elif "query_anything.emergency_calls" in line.lower():
                return line
    return "SELECT * FROM query_anything.emergency_calls;"  # 預設值改為列出所有記錄

def summarize_sql(sql: str, params=None):
    if not params:
        params = {}
    return f"根據 '{params.get('question', 'default input')}' 查詢的結果"