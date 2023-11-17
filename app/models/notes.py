from pydantic import BaseModel, ConfigDict

from app.prisma.models import Note as _Note


class Note:
    @classmethod
    async def read_all(cls) -> list[_Note]:
        return await _Note.prisma().find_many(include={"notebook": True})

    @classmethod
    async def read_by_id(cls, id_: int) -> _Note | None:
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


class NoteSchema(BaseModel):
    id: int
    title: str
    content: str
    notebook_id: int
    notebook_title: str

    model_config = ConfigDict(from_attributes=True)
