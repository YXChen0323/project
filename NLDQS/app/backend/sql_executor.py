import pandas as pd
import os
from sqlalchemy import create_engine

def execute_sql(file_path: str, sql: str) -> pd.DataFrame:
    """
    Executes an SQL query against a database or a file (CSV, Excel).

    Args:
        file_path (str): The path to the database file or data file.
        sql (str): The SQL query to execute.

    Returns:
        pd.DataFrame: The result of the SQL query as a Pandas DataFrame.

    Raises:
        ValueError: If the file format is not supported.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".db":
        return execute_sqlite(file_path, sql)
    elif ext in [".csv", ".xlsx"]:
        return execute_sql_in_memory(file_path, sql)
    else:
        raise ValueError("Unsupported file format")

def execute_sqlite(db_path: str, sql: str) -> pd.DataFrame:
    """
    Executes an SQL query against an SQLite database.

    Args:
        db_path (str): The path to the SQLite database file.
        sql (str): The SQL query to execute.

    Returns:
        pd.DataFrame: The result of the SQL query as a Pandas DataFrame.

    Raises:
        RuntimeError: If there is an error executing the SQL query.
    """
    engine = create_engine(f"sqlite:///{db_path}")
    try:
        df = pd.read_sql_query(sql, con=engine)
    except Exception as e:
        raise RuntimeError(f"SQL query error: {e}")
    return df

def execute_sql_in_memory(file_path: str, sql: str) -> pd.DataFrame:
    """
    Executes an SQL query against a CSV or Excel file by loading the data into an in-memory SQLite database.

    Args:
        file_path (str): The path to the CSV or Excel file.
        sql (str): The SQL query to execute.

    Returns:
        pd.DataFrame: The result of the SQL query as a Pandas DataFrame.

    Raises:
        RuntimeError: If there is an error executing the SQL query.
    """
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
        raise RuntimeError(f"SQL query error: {e}")
    return result
