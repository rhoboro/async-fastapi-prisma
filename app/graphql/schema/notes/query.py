from typing import Any

import graphene

from app import models

from .schema import Note


class GetNoteQuery(graphene.ObjectType):
    note = graphene.Field(Note, id_=graphene.Int(name="id", required=True))

    @staticmethod
    async def resolve_note(parent: Any, info: graphene.ResolveInfo, id_: int) -> Note:
        note = await models.Note.read_by_id(id_)
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
        notes = await models.Note.read_all()
        return [
            Note(
                id=note.id,
                title=note.title,
                content=note.content,
                notebook_id=note.notebook_id,
                notebook=note.notebook,
            )
            for note in notes
        ]
