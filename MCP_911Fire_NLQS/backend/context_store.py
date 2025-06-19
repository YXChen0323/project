import sqlite3
from datetime import datetime
import os

DB_PATH = os.getenv("CONTEXT_DB_PATH", "context.db")

# 初始化資料表（第一次執行用）
def init_context_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS context_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                question TEXT,
                generated_sql TEXT,
                result_summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# 儲存一筆紀錄
def save_query_record(user_id: str, question: str, sql: str, summary: str):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO context_history (user_id, question, generated_sql, result_summary)
            VALUES (?, ?, ?, ?)
        """, (user_id, question, sql, summary))
        conn.commit()

# 查詢歷史紀錄
def get_recent_queries(user_id: str, limit: int = 5):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT question, generated_sql, result_summary, created_at
            FROM context_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))
        return c.fetchall()
