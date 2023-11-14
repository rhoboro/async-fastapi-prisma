from typing import Any, Optional

import graphene
from graphql import GraphQLError

from app import models

from .schema import Notebook


class CreateNotebooksMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        notes = graphene.NonNull(graphene.List(graphene.NonNull(graphene.Int)))

    Output = graphene.NonNull(Notebook)

    @staticmethod
    async def mutate(parent: Any, title: str, notes: list[int]) -> Notebook:
        notes_ = await models.Note.read_by_ids(notes)
        notebook = await models.Notebook.create(title=title, notes=notes_)
        return Notebook(
            id=notebook.id,
            title=notebook.title,
            notes=notebook.notes,
        )


class UpdateNotebooksMutation(graphene.Mutation):
    class Arguments:
        id_ = graphene.Int(required=True, name="id")
        title = graphene.String(required=True)
        notes = graphene.NonNull(graphene.List(graphene.NonNull(graphene.Int)))

    Output = graphene.NonNull(Notebook)

    @staticmethod
    async def mutate(parent: Any, id_: int, title: str, notes: list[int]) -> Notebook:
        exist = await models.Notebook.read_by_id(id_, include_notes=False)
        if not exist:
            raise GraphQLError("NotFound")

        notes_ = await models.Note.read_by_ids(notes)
        notebook = await models.Notebook.update(exist, title, notes_)
        return Notebook(
            id=notebook.id,
            title=notebook.title,
            notes=notebook.notes,
        )


class DeleteNotebooksMutation(graphene.Mutation):
    class Arguments:
        id_ = graphene.Int(required=True, name="id")

    Output = Notebook

    @staticmethod
    async def mutate(parent: Any, id_: int) -> Optional[Notebook]:
        notebook = await models.Notebook.read_by_id(id_)
        if not notebook:
            return

        await models.Notebook.delete(notebook)
        return None


class NotebooksMutation(graphene.ObjectType):
    create_notebook = CreateNotebooksMutation.Field()
    update_notebook = UpdateNotebooksMutation.Field()
    delete_notebook = DeleteNotebooksMutation.Field()
