from fastapi import FastAPI, Request, UploadFile, File, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from llm_interface import query_llm
from sql_executor import run_sql_query
import psycopg2
import csv
import json
import io
import os
import pandas as pd

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定 ['http://localhost:3000']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCHEMA_NAME = "query_anything"

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        ext = os.path.splitext(file.filename)[1].lower()
        table_name = ""
        headers = []
        data = []

        # ✅ 處理 .csv
        if ext == ".csv":
            table_name = os.path.splitext(file.filename)[0].strip().replace(" ", "_").lower()
            content = await file.read()
            decoded = content.decode('utf-8')
            reader = csv.reader(io.StringIO(decoded))
            rows = list(reader)

            if not rows:
                return {"message": "CSV 檔案為空"}

            # ✅ 清除不可見字元的欄位名稱
            headers = [h.strip().replace('\ufeff', '').replace('\u200b', '') for h in rows[0]]
            data = rows[1:]

        # ✅ 處理 .xlsx
        elif ext == ".xlsx":
            content = await file.read()
            df = pd.read_excel(io.BytesIO(content), engine='openpyxl')
            if df.empty:
                return {"message": "Excel 檔案為空"}

            table_name = df.columns[0] if df.columns[0] else "excel_table"
            table_name = str(table_name).strip().replace(" ", "_").lower()

            # ✅ 清除不可見字元的欄位名稱
            headers = [str(col).strip().replace('\ufeff', '').replace('\u200b', '') for col in df.columns]
            data = df.values.tolist()

        else:
            return {"message": "只支援 .csv 或 .xlsx 檔案"}

        # 🔌 寫入 PostgreSQL
        conn = psycopg2.connect(
            dbname="mydatabase",
            user="user",
            password="123456",
            host="postgres_service",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute(f'CREATE SCHEMA IF NOT EXISTS "query_anything";')

        col_defs = ", ".join([f'"{h}" TEXT' for h in headers])
        cur.execute(f'CREATE TABLE IF NOT EXISTS "query_anything"."{table_name}" ({col_defs});')

        placeholders = ", ".join(["%s"] * len(headers))
        column_names = ", ".join([f'"{col}"' for col in headers])
        insert_sql = f'''
            INSERT INTO "query_anything"."{table_name}" ({column_names})
            VALUES ({placeholders})
        '''
        cur.executemany(insert_sql, data)

        conn.commit()
        conn.close()

        return {"message": f"成功匯入 {len(data)} 筆資料到 {table_name}"}

    except Exception as e:
        return {"message": f"錯誤：{str(e)}"}


@app.get("/list_tables")
def list_tables():
    try:
        SCHEMA_NAME = "query_anything"

        conn = psycopg2.connect(
            dbname="mydatabase",
            user="user",
            password="123456",
            host="postgres_service",
            port="5432"
        )
        cur = conn.cursor()
        # 使用 pg_catalog 更穩定且保證只抓 query_anything 的表
        cur.execute("""
            SELECT tablename
            FROM pg_catalog.pg_tables
            WHERE schemaname = %s
            ORDER BY tablename;
        """, (SCHEMA_NAME,))
        tables = [row[0] for row in cur.fetchall()]
        print("找到資料表：", tables)
        conn.close()

        return {"tables": tables}
    except Exception as e:
        return {"message": f"錯誤：{str(e)}"}

@app.post("/query")
async def query(request: Request):
    try:
        body = await request.json()
        query_text = body.get("query")
        table_name = body.get("table")

        if not query_text or not table_name:
            return {"message": "錯誤：缺少 query 或 table 參數"}

        # 取得欄位與範例資料
        def get_sample_row(table_name: str):
            conn = psycopg2.connect(
                dbname="mydatabase",
                user="user",
                password="123456",
                host="postgres_service",
                port="5432"
            )
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM "query_anything"."{table_name}" LIMIT 1')
            columns = [desc[0] for desc in cur.description]
            row = cur.fetchone()
            conn.close()
            return columns, row

        columns, sample_row = get_sample_row(table_name)
        sample_text = json.dumps(dict(zip(columns, sample_row)), ensure_ascii=False)


        prompt = f"""
        You are a database query assistant. Please convert the user's natural language question into a PostgreSQL query statement.

            📌 Table: query_anything.{table_name}

            📌 Column names: {', '.join(columns)}

            📌 Sample data (to understand column semantics):

            {sample_text}

            📌 Rules:

            SQL source table is query_anything.{table_name}
            Use single quotes for strings ('Apple')
            Use double quotes for column names with spaces ("Model Name")
            Use only the provided columns
            Map columns correctly based on semantics, e.g., Apple → Company Name
            Output only the SQL query, no explanations
            Question:

            "{query_text}"
        """.strip()

        # 送出 LLM
        sql = query_llm(prompt)

        # 執行 SQL 並格式化結果
        data = run_sql_query(sql)
        result = [dict(zip(data["columns"], row)) for row in data["rows"]]

        return {"sql": sql, "result": result}

    except Exception as e:
        return JSONResponse(content={"message": f"錯誤：{str(e)}"}, status_code=400)

