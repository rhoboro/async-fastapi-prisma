from typing import TYPE_CHECKING, Any

import graphene
from graphql import GraphQLError

from app import models

if TYPE_CHECKING:
    from ..notes import Note


class Notebook(graphene.ObjectType):
    id = graphene.String(required=True)
    title = graphene.String(required=True)
    notes = graphene.NonNull(graphene.List(graphene.NonNull("app.graphql.schema.notes.Note")))

    @staticmethod
    async def resolve_notes(parent: Any, info: graphene.ResolveInfo) -> list["Note"]:
        from ..notes import Note

        notes = getattr(parent, "notes", None)
        if not notes:
            notebook = await models.Notebook.read_by_id(parent.id, include_notes=True)
            if not notebook:
                raise GraphQLError("NotFound")
            notes = notebook.notes

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
