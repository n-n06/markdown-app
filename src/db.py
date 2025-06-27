from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from src.config import settings


engine = create_async_engine(
    url=settings.db_url_async,
    echo=True,  # logging
    pool_size=5, # connetcion count
    max_overflow=10 # additional connetion count
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()
