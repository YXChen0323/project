import pandas as pd
import os
from sqlalchemy import create_engine

def execute_sql(file_path: str, sql: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".db":
        return execute_sqlite(file_path, sql)
    elif ext in [".csv", ".xlsx"]:
        return execute_sql_in_memory(file_path, sql)
    else:
        raise ValueError("不支援的檔案格式")

def execute_sqlite(db_path: str, sql: str) -> pd.DataFrame:
    engine = create_engine(f"sqlite:///{db_path}")
    try:
        df = pd.read_sql_query(sql, con=engine)
    except Exception as e:
        raise RuntimeError(f"SQL 查詢錯誤：{e}")
    return df

def execute_sql_in_memory(file_path: str, sql: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    table_name = os.path.splitext(os.path.basename(file_path))[0]
    engine = create_engine("sqlite:///:memory:")
    df.to_sql(table_name, con=engine, index=False, if_exists="replace")

    try:
        result = pd.read_sql_query(sql, con=engine)
    except Exception as e:
        raise RuntimeError(f"SQL 查詢錯誤：{e}")
    return result
