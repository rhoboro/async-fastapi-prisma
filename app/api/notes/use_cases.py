from typing import AsyncIterator

from fastapi import Depends, HTTPException

from app.database import Prisma, get_db
from app.models import Note, Notebook, NoteSchema


class CreateNote:
    def __init__(self, session: Prisma = Depends(get_db)) -> None:
        self.async_session = session

    async def execute(self, notebook_id: int, title: str, content: str) -> NoteSchema:
        notebook = await Notebook.read_by_id(notebook_id)
        if not notebook:
            raise HTTPException(status_code=404)
        note = await Note.create(notebook.id, title, content)
        return NoteSchema.from_orm(note)


class ReadAllNote:
    def __init__(self, session: Prisma = Depends(get_db)) -> None:
        self.async_session = session

    async def execute(self) -> AsyncIterator[NoteSchema]:
        for note in await Note.read_all():
            yield NoteSchema.from_orm(note)


class ReadNote:
    def __init__(self, session: Prisma = Depends(get_db)) -> None:
        self.async_session = session

    async def execute(self, note_id: int) -> NoteSchema:
        note = await Note.read_by_id(note_id)
        if not note:
            raise HTTPException(status_code=404)
        return NoteSchema.from_orm(note)


class UpdateNote:
    def __init__(self, session: Prisma = Depends(get_db)) -> None:
        self.async_session = session

    async def execute(self, note_id: int, notebook_id: int, title: str, content: str) -> NoteSchema:
        note = await Note.read_by_id(note_id)
        if not note:
            raise HTTPException(status_code=404)

        if note.notebook_id != notebook_id:
            notebook = await Notebook.read_by_id(notebook_id)
            if not notebook:
                raise HTTPException(status_code=404)
            notebook_id = notebook.id
        else:
            notebook_id = note.notebook_id

        note = await Note.update(note, notebook_id=notebook_id, title=title, content=content)
        return NoteSchema.from_orm(note)


class DeleteNote:
    def __init__(self, session: Prisma = Depends(get_db)) -> None:
        self.async_session = session

    async def execute(self, note_id: int) -> None:
        note = await Note.read_by_id(note_id)
        if not note:
            return
        await Note.delete(note)
