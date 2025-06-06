import psycopg2

def run_sql_query(query: str):
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="user",
        password="123456",
        host="postgres_service",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    conn.close()
    return {"columns": columns, "rows": rows}
