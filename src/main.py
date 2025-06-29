from fastapi import FastAPI

from src.notes.router import router
from src.auth.router import auth_router

app = FastAPI()

app.include_router(router)
app.include_router(auth_router)
