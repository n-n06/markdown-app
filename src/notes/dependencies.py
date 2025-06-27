from fastapi import Depends
from src.db import AsyncSessionLocal

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
