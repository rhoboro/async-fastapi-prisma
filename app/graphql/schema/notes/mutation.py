from typing import Any, Optional

import graphene
from graphql import GraphQLError

from app import models

from .schema import Note


class CreateNotesMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        notebook_id = graphene.Int(required=True)

    Output = graphene.NonNull(Note)

    @staticmethod
    async def mutate(parent: Any, title: str, content: str, notebook_id: int):
        notebook = await models.Notebook.read_by_id(notebook_id)
        if not notebook:
            raise GraphQLError("NotFound")

        note = await models.Note.create(notebook.id, title=title, content=content)
        return Note(
            id=note.id,
            title=note.title,
            content=note.content,
            notebook_id=note.notebook_id,
            notebook=note.notebook,
        )


class UpdateNotesMutation(graphene.Mutation):
    class Arguments:
        id_ = graphene.Int(required=True, name="id")
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        notebook_id = graphene.Int(required=True)

    Output = graphene.NonNull(Note)

    @staticmethod
    async def mutate(parent: Any, id_: int, title: str, content: str, notebook_id: int):
        exist = await models.Note.read_by_id(id_)
        if not exist:
            raise GraphQLError("NotFound")

        notebook = await models.Notebook.read_by_id(notebook_id)
        if not notebook:
            raise GraphQLError("NotFound")

        note = await models.Note.update(
            exist, notebook_id=notebook.id, title=title, content=content
        )
        return Note(
            id=note.id,
            title=note.title,
            content=note.content,
            notebook_id=note.notebook_id,
            notebook=note.notebook,
        )


class DeleteNotesMutation(graphene.Mutation):
    class Arguments:
        id_ = graphene.Int(required=True, name="id")

    Output = Note

    @staticmethod
    async def mutate(parent: Any, id_: int) -> Optional[Note]:
        note = await models.Note.read_by_id(id_)
        if not note:
            return

        await models.Note.delete(note)
        return None


class NotesMutation(graphene.ObjectType):
    create_note = CreateNotesMutation.Field()
    update_note = UpdateNotesMutation.Field()
    delete_note = DeleteNotesMutation.Field()
