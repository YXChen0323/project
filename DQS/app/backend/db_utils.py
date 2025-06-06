import sqlite3
import pandas as pd
import os

def get_schema(file_path: str) -> str:
    """根據副檔名，自動使用正確表格名稱建立 schema"""
    ext = os.path.splitext(file_path)[1].lower()
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    if ext == ".db":
        return get_db_schema(file_path)
    elif ext == ".csv":
        return get_csv_schema(file_path, table_name=base_name)
    elif ext == ".xlsx":
        return get_excel_schema(file_path)
    else:
        return "不支援的檔案格式"

def get_db_schema(db_path: str) -> str:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    result = []
    for (table_name,) in tables:
        result.append(f"Table: {table_name}")
        columns = cursor.execute(f"PRAGMA table_info({table_name});").fetchall()
        for col in columns:
            result.append(f"  - {col[1]} ({col[2]})")  # col[1]:欄位名, col[2]:型別
    conn.close()
    return "\n".join(result)

def get_csv_schema(csv_path: str, table_name: str = "data_from_csv") -> str:
    df = pd.read_csv(csv_path, nrows=5)
    result = [f"Table: {table_name}"]
    for col, dtype in zip(df.columns, df.dtypes):
        result.append(f"  - {col} ({dtype})")
    return "\n".join(result)

def get_excel_schema(excel_path: str) -> str:
    xls = pd.ExcelFile(excel_path)
    result = []
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name, nrows=5)
        result.append(f"Table: {sheet_name}")
        for col, dtype in zip(df.columns, df.dtypes):
            result.append(f"  - {col} ({dtype})")
    return "\n".join(result)
