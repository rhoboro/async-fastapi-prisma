from typing import Any, Optional

from pydantic import BaseModel
from pydantic.utils import GetterDict

from app.models.notes import NoteSchema
from app.prisma.models import Note as _Note
from app.prisma.models import Notebook as _Notebook


class Notebook:
    @classmethod
    async def read_all(cls, include_notes: bool = False) -> list[_Notebook]:
        if include_notes:
            return await _Notebook.prisma().find_many(
                include={"notes": {"include": {"notebook": True}}}
            )
        else:
            return await _Notebook.prisma().find_many(include={"notes": False})

    @classmethod
    async def read_by_id(cls, id_: int, include_notes: bool = False) -> Optional[_Notebook]:
        return await _Notebook.prisma().find_unique(
            where={"id": id_}, include={"notes": include_notes}
        )

    @classmethod
    async def create(cls, title: str, notes: list[_Note]) -> _Notebook:
        if not notes:
            return await _Notebook.prisma().create(data={"title": title})

        return await _Notebook.prisma().create(
            data={"title": title, "notes": {"connect": [{"id": note.id} for note in notes]}},
            include={"notes": {"include": {"notebook": True}}},
        )

    @classmethod
    async def update(cls, notebook: _Notebook, title: str, notes: list[_Note]) -> _Notebook:
        updated = await _Notebook.prisma().update(
            where={"id": notebook.id},
            data={"title": title, "notes": {"set": [{"id": note.id} for note in notes]}},
            include={"notes": {"include": {"notebook": True}}},
        )
        if not updated:
            raise Exception("Unexpected State")
        return updated

    @classmethod
    async def delete(cls, notebook: _Notebook) -> None:
        await _Notebook.prisma().delete(where={"id": notebook.id})


class _NotebookSchemaGetter(GetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        if key == "notes":
            if not self._obj.notes:
                return []
            return [NoteSchema.from_orm(note) for note in self._obj.notes]

        return getattr(self._obj, key, default)


class NotebookSchema(BaseModel):
    id: int
    title: str
    notes: list[NoteSchema]

    class Config:
        orm_mode = True
        getter_dict = _NotebookSchemaGetter
