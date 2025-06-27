from fastapi import FastAPI

from src.notes.router import router

app = FastAPI()

app.include_router(router)

