from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re

def build_prompt(user_question: str, schema: str, sample_rows: list) -> str:
    """
    Constructs a prompt for the language model to generate SQL queries.

    Args:
        user_question (str): The user's question in natural language.
        schema (str): The database table schema.
        sample_rows (list): Sample rows from the table for context.

    Returns:
        str: A formatted prompt string for the language model.
    """
    lines = schema.strip().split("\n")
    table_name = "資料表"
    for line in lines:
        if line.startswith("Table: "):
            table_name = line.replace("Table: ", "").strip()
            break

    examples = ""
    for i, row in enumerate(sample_rows):
        examples += f"--- 樣本 {i+1} ---\n"
        examples += "\n".join([f"{k}: {v}" for k, v in row.items()])
        examples += "\n"

    first_row = sample_rows[0]
    recommended_conditions = "\n".join([f"{k}: {v}" for k, v in first_row.items()])

    return f"""你是一個 SQL 專家。請根據下列資料表結構與使用者問題，產生對應的 SQL 查詢語句。


            請注意，欄位名稱中如有括號，括號也必須包含在引號中，整體視為一個欄位名稱，不可拆開。
            你應根據問題中涉及的所有欄位，組成正確的 WHERE 條件式。
            條件值應盡可能來自下方的樣本資料中。

            請務必使用表格名稱 `{table_name}`，不要使用其他名稱。

            [資料表結構]
            {schema}

            [參考資料]
            {examples}

            [建議條件組合]
            {recommended_conditions}

            [使用者問題]
            {user_question}

            請只輸出一行 SQL 查詢語句，不要附加說明，也不要產生多段。
            [對應的 SQL]
            """

def quote_column_names(sql: str, schema: str) -> str:
    """
    Encloses column names in quotes within an SQL query.

    Args:
        sql (str): The SQL query string.
        schema (str): The database table schema.

    Returns:
        str: The modified SQL query with column names enclosed in quotes.
    """
    column_pattern = re.compile(r"- (.+?) \(")
    columns = column_pattern.findall(schema)
    for col in sorted(columns, key=len, reverse=True):
        quoted = f'"{col}"'
        if quoted in sql:
            continue
        pattern = rf'(?<!["\w]){re.escape(col)}(?![\w"])'
        sql = re.sub(pattern, quoted, sql)
    return sql

def patch_split_column(sql: str, schema: str) -> str:
    """
    Handles cases where column names are split incorrectly.

    Args:
        sql (str): The SQL query string.
        schema (str): The database table schema.

    Returns:
        str: The modified SQL query with patched column names.
    """
    column_pattern = re.compile(r"- (.+?) \(")
    columns = column_pattern.findall(schema)

    for col in columns:
        if "(" in col and ")" in col:
            full_col = col
            prefix = col.split("(")[0].strip()
            suffix = col.split("(")[1].replace(")", "").strip()

            pattern_func = rf'(\b\w+\b)\s*\(\s*"{re.escape(prefix)}"\s*\(\s*{re.escape(suffix)}\s*\)\s*\)'
            sql = re.sub(pattern_func, lambda m: f'{m.group(1)}("{full_col}")', sql)

            pattern_plain = rf'"{re.escape(prefix)}"\s*\(\s*{re.escape(suffix)}"\s*\)'
            sql = re.sub(pattern_plain, f'"{full_col}"', sql)

    return sql

def generate_sql(user_question: str, schema: str, sample_rows: list, model, tokenizer) -> str:
    """Generates an SQL query based on a user question, database schema, and sample rows.

    Args:
        user_question (str): The question asked by the user in natural language.
        schema (str): The schema of the database table, including table name and column definitions.
        sample_rows (list): A list of sample rows from the database table, used to provide context for the language model.
        model: The pre-trained language model used to generate the SQL query.
        tokenizer: The tokenizer associated with the language model.

    Returns:
        str: The generated SQL query as a string, refined for compatibility with the database.
    """
    prompt = build_prompt(user_question, schema, sample_rows)

    messages = [
        {"role": "system", "content": "你是一個 SQL 專家。你會根據使用者的問題與資料表結構，產生對應的 SQL 查詢語句。"},
        {"role": "user", "content": prompt}
    ]

    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt")
    model_inputs = {k: v.to(model.device) for k, v in model_inputs.items()}

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512
    )

    input_ids = model_inputs["input_ids"]
    output_ids = [output[len(input_ids[i]):] for i, output in enumerate(generated_ids)]
    response = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
    response = response.replace("```sql", "").replace("```", "").strip()

    sql_output = quote_column_names(response, schema)
    sql_output = patch_split_column(sql_output, schema)

    lines = schema.strip().split("\n")
    table_name = None
    for line in lines:
        if line.startswith("Table: "):
            table_name = line.replace("Table: ", "").strip()
            break

    if table_name and " " in table_name and f'"{table_name}"' not in sql_output:
        sql_output = sql_output.replace(table_name, f'"{table_name}"')

    return sql_output

def summarize_result(question: str, result_df, model, tokenizer) -> str:
    """
    Summarizes the result of a data query using natural language.

    Args:
        question (str): The user's question.
        result_df: The query result as a Pandas DataFrame.
        model: The language model.
        tokenizer: The tokenizer.

    Returns:
        str: A natural language summary of the query result.
    """
    import re
    from langdetect import detect

    try:
        lang = detect(question)
    except:
        lang = "en"

    preview_text = result_df.head(3).to_string(index=False)

    prompt = f"""你是一位資料助理，擅長用自然口語方式說明資料查詢結果。

    請根據使用者的提問與下方查詢結果，給出一段清楚、自然、完整的回覆。
    不需要再列出表格內容，也不需要說明你是 AI，只要直接講答案就好。

    使用者問題：
    {question}

    查詢結果：
    {preview_text}

    請以{'中文' if lang == 'zh' else '英文'}自然語言直接回答：
    """

    messages = [
        {"role": "system", "content": "你是一個擅長自然語言摘要資料的助手。"},
        {"role": "user", "content": prompt}
    ]

    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt", padding=True, truncation=True)
    model_inputs = {k: v.to(model.device) for k, v in model_inputs.items()}

    outputs = model.generate(**model_inputs, max_new_tokens=150)
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

    lines = decoded.strip().split("\n")
    final_line = lines[-1].strip() if lines else decoded.strip()
    final_line = re.sub(r"^assistant[:：]?", "", final_line, flags=re.IGNORECASE).strip()

    return final_line
