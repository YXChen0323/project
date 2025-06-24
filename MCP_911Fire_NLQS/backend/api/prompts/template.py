def get_template(task: str) -> str:
    if task == "generate_sql":
        return """You are a SQL assistant for a PostgreSQL database.
{history}

User: {input}
Please generate a valid SQL query based on the user's request, using the 'query_anything.emergency_calls' table. 
- If the request involves listing records (e.g., 'list' or 'show all'), use SELECT * with appropriate WHERE clauses for filtering (e.g., location, status).
- If the request involves counting records (e.g., 'how many' or 'total number'), use COUNT(*).
Use only the original column names from the 'emergency_calls' table (e.g., id, call_time, location, status).
Only output the SQL query without explanations.
"""
    elif task == "explain_code":
        return """You are a code expert.
{history}

User: {input}
Please explain the following code clearly.
"""
    elif task == "chat":
        return """You are a helpful assistant.
{history}

User: {input}
Reply briefly and naturally.
"""
    else:
        return "{input}"