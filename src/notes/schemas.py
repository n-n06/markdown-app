from datetime import datetime
from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    last_edited: datetime

    class Config:
        orm_model=True

class GrammarCorrection(BaseModel):
    start: int
    end: int
    mistake: str
    replacements: list[str]
