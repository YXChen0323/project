from api.context.memory import add  # 假設 api 是根模組
from .models import sql_models
from .prompts.prompt_builder import build_prompt
from . import sql_exec

def route_task(method: str, params: dict):
    user_id = params.get("user", "default")
    model = params.get("model", "sqlcoder")

    if method == "generate_sql":
        question = params["question"]
        prompt = build_prompt("generate_sql", question, user_id)
        result = sql_models.query(model, prompt, params)

        sql = result["sql"]
        summary = result["summary"]
        data = sql_exec.run_query(sql)

        # 更新記憶
        add(user_id, "user", question)
        add(user_id, "model", f"SQL: {sql}, Summary: {summary}")

        return {
            "model_used": model,
            "sql": sql,
            "summary": summary,
            "data": data
        }

    raise ValueError(f"Unsupported method: {method}")