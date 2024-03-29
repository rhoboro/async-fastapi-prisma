from typing import AsyncIterator

from fastapi import HTTPException

from app.database import Database
from app.models import Note, Notebook, NotebookSchema


class CreateNotebook:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def execute(self, title: str, notes: list[int]) -> NotebookSchema:
        exist_notes = [n for n in await Note.read_by_ids(note_ids=notes)]
        if len(exist_notes) != len(notes):
            raise HTTPException(status_code=404)
        notebook = await Notebook.create(title, exist_notes)
        return NotebookSchema.model_validate(notebook)


class ReadAllNotebook:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def execute(self) -> AsyncIterator[NotebookSchema]:
        for notebook in await Notebook.read_all(include_notes=True):
            yield NotebookSchema.model_validate(notebook)


class ReadNotebook:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def execute(self, notebook_id: int) -> NotebookSchema:
        notebook = await Notebook.read_by_id(notebook_id, include_notes=True)
        if not notebook:
            raise HTTPException(status_code=404)
        return NotebookSchema.model_validate(notebook)


class UpdateNotebook:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def execute(self, notebook_id: int, title: str, notes: list[int]) -> NotebookSchema:
        notebook = await Notebook.read_by_id(notebook_id, include_notes=True)
        if not notebook:
            raise HTTPException(status_code=404)

        exist_notes = [n for n in await Note.read_by_ids(note_ids=notes)]
        if len(exist_notes) != len(notes):
            raise HTTPException(status_code=404)

        notebook = await Notebook.update(notebook, title, exist_notes)
        return NotebookSchema.model_validate(notebook)


class DeleteNotebook:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def execute(self, notebook_id: int) -> None:
        notebook = await Notebook.read_by_id(notebook_id)
        if not notebook:
            return
        await Notebook.delete(notebook)
