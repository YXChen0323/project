from fastapi import APIRouter
from pydantic import BaseModel
from model_router import call_llm_with_prompt
from prompt_template import build_prompt
from database import execute_sql
from context_store import save_query_record

router = APIRouter()

class QueryRequest(BaseModel):
    user_id: str
    query: str
    model: str = "phi3"

@router.post("/query")
async def query_endpoint(req: QueryRequest):
    try:
        # 1. 建立提示語（含歷史）
        prompt = build_prompt(req.query, user_id=req.user_id)

        # 2. 呼叫 LLM 模型轉換成 SQL
        sql = call_llm_with_prompt(prompt, model=req.model)

        # 3. 執行 SQL 查詢
        result = execute_sql(sql)

        # 4. 儲存查詢紀錄
        save_query_record(req.user_id, req.query, sql, str(result))

        # 5. 回傳成功結果
        return {
            "sql": sql,
            "result": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }
