from typing import Any

import graphene

from app.use_cases.notes import CreateNote, DeleteNote, UpdateNote

from .schema import Note


class CreateNoteMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        notebook_id = graphene.Int(required=True)

    Output = graphene.NonNull(Note)

    @staticmethod
    async def mutate(
        parent: Any,
        info: graphene.ResolveInfo,
        notebook_id: int,
        title: str,
        content: str,
    ) -> Note:
        note = await CreateNote(info.context["db"]).execute(notebook_id, title, content)
        return Note(
            id=note.id,
            title=note.title,
            content=note.content,
            notebook_id=note.notebook_id,
            notebook=note.notebook,
        )


class UpdateNoteMutation(graphene.Mutation):
    class Arguments:
        id_ = graphene.Int(required=True, name="id")
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        notebook_id = graphene.Int(required=True)

    Output = graphene.NonNull(Note)

    @staticmethod
    async def mutate(
        parent: Any,
        info: graphene.ResolveInfo,
        id_: int,
        title: str,
        content: str,
        notebook_id: int,
    ) -> Note:
        note = await UpdateNote(info.context["db"]).execute(id_, notebook_id, title, content)
        return Note(
            id=note.id,
            title=note.title,
            content=note.content,
            notebook_id=note.notebook_id,
            notebook=note.notebook,
        )


class DeleteNoteMutation(graphene.Mutation):
    class Arguments:
        id_ = graphene.Int(required=True, name="id")

    Output = Note

    @staticmethod
    async def mutate(parent: Any, info: graphene.ResolveInfo, id_: int) -> None:
        return await DeleteNote(info.context["db"]).execute(id_)


class NotesMutation(graphene.ObjectType):
    create_note = CreateNoteMutation.Field()
    update_note = UpdateNoteMutation.Field()
    delete_note = DeleteNoteMutation.Field()
