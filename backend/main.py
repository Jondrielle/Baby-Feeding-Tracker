from fastapi import FastAPI
from backend.routes.feed import router
from backend.database import create_db_and_tables

app = FastAPI()

app.include_router(router)


    