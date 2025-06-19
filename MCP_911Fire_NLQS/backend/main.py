from fastapi import FastAPI
from query_api import router as query_router
from context_store import init_context_db

init_context_db()
app = FastAPI()
app.include_router(query_router)
