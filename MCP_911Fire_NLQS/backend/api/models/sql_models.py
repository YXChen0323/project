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
            if "query_anything.emergency_calls" in line.lower():
                return line
    return "[No SQL generated]"  # 改為明確的佔位符，替代預設 SQL

def summarize_sql(sql: str, params=None):
    if not params:
        params = {}
    return f"根據 '{params.get('question', 'default input')}' 查詢的結果" if sql != "[No SQL generated]" else "模型未生成有效的 SQL 查詢"