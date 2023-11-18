from typing import Any

import graphene

from app.use_cases.notebooks import CreateNotebook, DeleteNotebook, UpdateNotebook

from .schema import Notebook


class CreateNotebookMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        notes = graphene.NonNull(graphene.List(graphene.NonNull(graphene.Int)))

    Output = graphene.NonNull(Notebook)

    @staticmethod
    async def mutate(
        parent: Any, info: graphene.ResolveInfo, title: str, notes: list[int]
    ) -> Notebook:
        notebook = await CreateNotebook(info.context["db"]).execute(title, notes)
        return Notebook(
            id=notebook.id,
            title=notebook.title,
            notes=notebook.notes,
        )


class UpdateNotebookMutation(graphene.Mutation):
    class Arguments:
        id_ = graphene.Int(required=True, name="id")
        title = graphene.String(required=True)
        notes = graphene.NonNull(graphene.List(graphene.NonNull(graphene.Int)))

    Output = graphene.NonNull(Notebook)

    @staticmethod
    async def mutate(
        parent: Any, info: graphene.ResolveInfo, id_: int, title: str, notes: list[int]
    ) -> Notebook:
        notebook = await UpdateNotebook(info.context["db"]).execute(id_, title, notes)
        return Notebook(
            id=notebook.id,
            title=notebook.title,
            notes=notebook.notes,
        )


class DeleteNotebookMutation(graphene.Mutation):
    class Arguments:
        id_ = graphene.Int(required=True, name="id")

    Output = Notebook

    @staticmethod
    async def mutate(parent: Any, info: graphene.ResolveInfo, id_: int) -> None:
        return await DeleteNotebook(info.context["db"]).execute(id_)


class NotebooksMutation(graphene.ObjectType):
    create_notebook = CreateNotebookMutation.Field()
    update_notebook = UpdateNotebookMutation.Field()
    delete_notebook = DeleteNotebookMutation.Field()
