from aiocache.decorators import cached
from aiocache.serializers import JsonSerializer
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.notes.models import Note
from src.notes.schemas import GrammarCorrection, NoteCreate, NoteOut, NoteUpdate
from src.notes.service import GrammarService, render
from src.auth.dependencies import current_active_user
from src.auth.models import User
from src.redis.service import make_key, redis_cache


router = APIRouter(prefix="/notes", tags=["Notes"])
grammar = GrammarService()


@router.post("/upload")
async def upload_file(
    file: UploadFile, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(current_active_user)
):

    if file.content_type != "text/markdown":
        raise HTTPException( 
            status_code=400, detail="Provided file is not a Markdown file"
        )    

    content = (await file.read()).decode("utf-8")
    note = Note(title=file.filename, content=content, user_id=current_user.id)
    db.add(note)
    await db.commit()
    await db.refresh(note)

    return note


@router.post("/", response_model=NoteOut, status_code=201)
async def create_note(
    note_data : NoteCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    note = Note(
        title=note_data.title,
        content=note_data.content,
        user_id=current_user.id
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note
    

@router.get("/", response_model=list[NoteOut])
async def list_notes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    result = await db.execute(
        select(Note.id, Note.title, Note.created_at, Note.last_edited).where(
            Note.user_id==current_user.id
        )
    )
    rows = result.all()

    return [
        NoteOut(id=row.id, title=row.title, 
                content="", created_at=row.created_at,
                last_edited=row.last_edited)
        for row in rows
    ]


@router.get("/{note_id}", response_model=NoteOut)
async def get_note(
    note_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    result = await db.execute(select(Note).where(
        Note.id == note_id, Note.user_id == current_user.id
    ))
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.get("/{note_id}/render/", response_class=HTMLResponse)
async def render_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    result = await db.execute(select(Note).where(
        Note.id == note_id, Note.user_id == current_user.id
    ))
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return render(note)


@router.put("/{note_id}", response_model=NoteOut)
async def update_note(
    note_id: int, 
    note_data: NoteCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """Replaces everything - uses PUT method"""
    
    result = await db.execute(select(Note).where(
        Note.id == note_id, Note.user_id == current_user.id
    ))
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = note_data.title
    note.content = note_data.content

    await db.commit()
    await db.refresh(note)

    return note


@router.patch("/{note_id}", response_model=NoteOut)
async def edit_note(
    note_id: int, 
    note_data: NoteUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """Replaces either title or content or both :)"""

    result = await db.execute(select(Note).where(
        Note.id == note_id, Note.user_id == current_user.id
    ))
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note_data.title is None and note_data.content is None:
        raise HTTPException(
            status_code=400, detail="Provide either title or content"
        )


    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content
    

    await db.commit()
    await db.refresh(note)

    return note


@cached(redis_cache, key_builder=make_key, serializer=JsonSerializer)
@router.post("/{note_id}/grammar/", response_model=list[GrammarCorrection])
async def check_grammar(
    note_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """Replaces either title or content or both :)"""

    db_result = await db.execute(select(Note).where(
        Note.id == note_id, Note.user_id == current_user.id
    ))
    note = db_result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    grammar_check_result = grammar.check_grammar(note.content)

    return grammar_check_result
