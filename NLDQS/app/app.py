import streamlit as st
import os
from backend.db_utils import *
from backend.llm_interface import *
from backend.sql_executor import *
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Disable Streamlit watcher to prevent reloads
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Custom CSS for styling the Streamlit app
st.markdown("""
    <style>
    .main-title {font-size:2.5rem; font-weight:700; color:#4F8BF9;}
    .sidebar-title {font-size:1.3rem; font-weight:600;}
    .stButton>button {background:#4F8BF9; color:white;}
    input[type="text"] {
        padding: 0.5rem;
        font-size: 1.1rem;
    }
    div[data-testid="stTabs"] {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Adjust padding to provide a wider layout
st.markdown("<style>div.block-container {padding-left:5rem; padding-right:5rem; max-width: 100% !important;}</style>", unsafe_allow_html=True)

@st.cache_resource
def load_model_once():
    """
    Loads the language model and tokenizer once to improve performance.
    Cached using Streamlit's resource caching to prevent reloading on each run.
    """
    MODEL_PATH = "./llm/model"
    TOKENIZER_PATH = "./llm/tokenizer"
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        trust_remote_code=True,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    ).to("cuda" if torch.cuda.is_available() else "cpu")
    return tokenizer, model

# Load the tokenizer and model
tokenizer, model = load_model_once()

def main():
    """
    Main function to run the Streamlit application.
    """
    # Set the main title of the application
    st.markdown('<div class="main-title">📊 Natural Language Database Query System</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Sidebar for file upload, selection, and query input
    with st.sidebar:
        st.markdown('<div class="sidebar-title">📁 Select or Upload Database</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload a database file (.csv, .xlsx, .db)", type=["csv", "xlsx", "db"])
        if uploaded_file:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            st.success(f"Uploaded: {uploaded_file.name}")

        files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith((".csv", ".xlsx", ".db"))]
        selected_file = st.selectbox("Select a file", files)

        st.markdown('<div class="sidebar-title">🧠 Natural Language Query</div>', unsafe_allow_html=True)
        user_input = st.text_input("Enter your query:")

        # Submit button to process the query
        if st.button("Submit Query") and user_input:
            st.session_state["pending_query"] = {"input": user_input, "file": selected_file}

        # Display query history
        st.markdown('<div class="sidebar-title">Query History</div>', unsafe_allow_html=True)
        if "history" not in st.session_state:
            st.session_state.history = []
        with st.expander("Show History", expanded=True):
            for i, item in enumerate(reversed(st.session_state.history[-10:])):
                index = len(st.session_state.history) - i
                if isinstance(item, dict) and "question" in item and "sql" in item:
                    st.markdown(f"**{index}. {item['question']}**")
                    st.code(item["sql"], language="sql")
                    if "result" in item:
                        st.dataframe(pd.DataFrame(item["result"]), use_container_width=True)
        # Button to clear the query history
        if st.button("🔄 Clear History"):
            st.session_state.history.clear()
            st.rerun()

    # Process the pending query
    if "pending_query" in st.session_state:
        user_input = st.session_state["pending_query"]["input"]
        selected_file = st.session_state["pending_query"]["file"]
        del st.session_state["pending_query"]

        # Execute the query and display results
        with st.spinner("Generating and executing query..."):
            target_file = os.path.join(UPLOAD_DIR, selected_file)
            schema = get_schema(target_file)
            if selected_file.endswith(".xlsx"):
                df_preview = pd.read_excel(target_file)
            elif selected_file.endswith(".csv"):
                df_preview = pd.read_csv(target_file)
            else:
                import sqlite3
                conn = sqlite3.connect(target_file)
                cursor = conn.cursor()
                first_table = cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name LIMIT 1"
                ).fetchone()
                if first_table:
                    df_preview = pd.read_sql_query(
                        f'SELECT * FROM "{first_table[0]}" LIMIT 5', conn
                    )
                else:
                    df_preview = pd.DataFrame()
                conn.close()

            sample_rows = df_preview.head(5).to_dict(orient="records")

            sql_query = generate_sql(user_input, schema, sample_rows, model, tokenizer)

            try:
                result_df = execute_sql(target_file, sql_query)

                # Display SQL query and results
                st.markdown("### 📝 SQL")
                st.code(sql_query, language="sql")

                st.markdown("### 📄 Result")
                st.dataframe(result_df)

                # Summarize the result using the language model
                from backend.llm_interface import summarize_result
                summary = summarize_result(user_input, result_df, model, tokenizer)
                st.markdown("### 🤖 Summary Answer")
                st.success(summary)

                # Store the query and result in history
                st.session_state.history.append({
                    "question": user_input,
                    "sql": sql_query,
                    "result": result_df.head(5).to_dict(orient="records")
                })

            except Exception as e:
                st.error(f"Query error: {e}")

# Run the main function
if __name__ == "__main__":
    main()
