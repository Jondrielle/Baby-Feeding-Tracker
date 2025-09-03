from fastapi import FastAPI
from backend.routes.feed import router

app = FastAPI()

app.include_router(router)
