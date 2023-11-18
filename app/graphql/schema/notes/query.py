from typing import Any

import graphene

from app.use_cases.notes import ReadAllNote, ReadNote

from .schema import Note


class GetNoteQuery(graphene.ObjectType):
    note = graphene.Field(Note, id_=graphene.Int(name="id", required=True))

    @staticmethod
    async def resolve_note(parent: Any, info: graphene.ResolveInfo, id_: int) -> Note:
        note = await ReadNote(info.context["db"]).execute(id_)
        return Note(
            id=note.id,
            title=note.title,
            content=note.content,
            notebook_id=note.notebook_id,
        )


class ListNotesQuery(graphene.ObjectType):
    all_notes = graphene.NonNull(graphene.List(graphene.NonNull(Note)))

    @staticmethod
    async def resolve_all_notes(parent: Any, info: graphene.ResolveInfo) -> list[Note]:
        return [
            Note(
                id=note.id,
                title=note.title,
                content=note.content,
                notebook_id=note.notebook_id,
                notebook=note.notebook,
            )
            async for note in ReadAllNote(info.context["db"]).execute()
        ]
