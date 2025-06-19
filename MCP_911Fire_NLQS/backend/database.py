import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_NAME = os.getenv("DB_NAME", "mydatabase")

# ✅ 簡單過濾規則
def is_safe_sql(sql: str) -> bool:
    allowed_prefix = sql.strip().lower().startswith("select")
    forbidden_keywords = ["drop", "delete", "alter", "update", "insert", ";--"]
    return allowed_prefix and not any(k in sql.lower() for k in forbidden_keywords)

# ✅ 執行 SQL 查詢
def execute_sql(sql: str):
    if not is_safe_sql(sql):
        raise ValueError("不允許的 SQL 查詢，僅支援安全的 SELECT 語句。")

    try:
        with psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                return rows
    except Exception as e:
        raise RuntimeError(f"資料庫查詢失敗：{e}")
