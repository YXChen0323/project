from context_store import get_recent_queries

def build_prompt(user_query: str, user_id: str = "guest", task_type: str = "sql_query") -> str:
    # 抓取最近 3 筆歷史作為上下文（可改成 5）
    history = get_recent_queries(user_id, limit=3)

    context_lines = []
    for i, (q, sql, _, _) in enumerate(history):
        context_lines.append(f"【歷史提問 {i+1}】：{q}\n【SQL】：{sql}\n")

    history_context = "\n".join(context_lines) if context_lines else "（無歷史紀錄）"

    # 範本組合
    if task_type == "sql_query":
        return f"""你是一個專業的 SQL 查詢產生器，請使用 PostgreSQL 語法。

                你會接收到使用者的問題與部分歷史查詢紀錄，請根據語意判斷是否延續上下文，並產出一段 SQL 查詢語句。
                請**只**輸出 SQL，不要任何說明。

                使用者問題：
                {user_query}

                歷史查詢紀錄：
                {history_context}
                """
    else:
        raise ValueError(f"不支援的任務類型：{task_type}")
