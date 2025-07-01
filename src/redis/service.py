from hashlib import sha256

import redis
from aiocache import RedisCache
from aiocache.serializers import JsonSerializer

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.dependencies import current_active_user
from src.db import get_db
from src.notes.models import Note

redis_client = redis.Redis(host="127.0.0.1", port=6379)
redis_cache = RedisCache(redis_client, namespace="main")


async def make_key(
    note_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    db_result = await db.execute(select(Note).where(
        Note.id == note_id, Note.user_id == current_user.id
    ))
    note = db_result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return sha256(note.content.encode("ascii"))
