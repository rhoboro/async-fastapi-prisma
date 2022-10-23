from typing import Any, Optional

from pydantic import BaseModel
from pydantic.utils import GetterDict

from app.prisma.models import Note as _Note


class Note:
    @classmethod
    async def read_all(cls) -> list[_Note]:
        return await _Note.prisma().find_many(include={"notebook": True})

    @classmethod
    async def read_by_id(cls, id_: int) -> Optional[_Note]:
        return await _Note.prisma().find_unique(where={"id": id_}, include={"notebook": True})

    @classmethod
    async def read_by_ids(cls, note_ids: list[int]) -> list[_Note]:
        return await _Note.prisma().find_many(
            where={"id": {"in": note_ids}}, include={"notebook": True}
        )

    @classmethod
    async def create(cls, notebook_id: int, title: str, content: str) -> _Note:
        return await _Note.prisma().create(
            data={"title": title, "content": content, "notebook_id": notebook_id},
            include={"notebook": True},
        )

    @classmethod
    async def update(cls, note: _Note, notebook_id: int, title: str, content: str) -> _Note:
        updated = await _Note.prisma().update(
            where={"id": note.id},
            data={"notebook": {"connect": {"id": notebook_id}}, "title": title, "content": content},
            include={"notebook": True},
        )
        if not updated:
            raise Exception("Unexpected State")

        return updated

    @classmethod
    async def delete(cls, note: _Note) -> None:
        await _Note.prisma().delete(where={"id": note.id})


class _NoteSchemaGetter(GetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        if key == "notebook_title":
            if not self._obj.notebook:
                raise Exception(f"{self._obj} must include notebook")
            return self._obj.notebook.title

        return getattr(self._obj, key, default)


class NoteSchema(BaseModel):
    id: int
    title: str
    content: str
    notebook_id: int
    notebook_title: str

    class Config:
        orm_mode = True
        getter_dict = _NoteSchemaGetter
