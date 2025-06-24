import psycopg2
import os

DB_HOST = os.getenv("POSTGRES_HOST", "postgres_service")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "mydatabase")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "123456")

def run_query(sql: str):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        cur.execute(sql)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        result = [dict(zip(colnames, row)) for row in rows]

        cur.close()
        conn.close()
        return result

    except Exception as e:
        print("SQL 查詢失敗：", e)
        return []