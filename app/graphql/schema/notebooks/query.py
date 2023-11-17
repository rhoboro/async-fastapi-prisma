from typing import Any

import graphene

from app import models

from .schema import Notebook


class GetNotebookQuery(graphene.ObjectType):
    notebook = graphene.Field(Notebook, id_=graphene.Int(name="id", required=True))

    @staticmethod
    async def resolve_notebook(parent: Any, info: graphene.ResolveInfo, id_: int) -> Notebook:
        notebook = await models.Notebook.read_by_id(id_, include_notes=True)
        return Notebook(
            id=notebook.id,
            title=notebook.title,
            notes=notebook.notes,
        )


class ListNotebooksQuery(graphene.ObjectType):
    all_notebooks = graphene.NonNull(graphene.List(graphene.NonNull(Notebook)))

    @staticmethod
    async def resolve_all_notebook(parent: Any, info: graphene.ResolveInfo) -> list[Notebook]:
        notebooks = await models.Notebook.read_all(include_notes=True)
        return [
            Notebook(
                id=notebook.id,
                title=notebook.title,
                notes=notebook.notes,
            )
            for notebook in notebooks
        ]
