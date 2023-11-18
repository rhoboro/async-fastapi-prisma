from typing import Any

import graphene

from app.use_cases.notebooks import ReadAllNotebook, ReadNotebook

from .schema import Notebook


class GetNotebookQuery(graphene.ObjectType):
    notebook = graphene.Field(Notebook, id_=graphene.Int(name="id", required=True))

    @staticmethod
    async def resolve_notebook(parent: Any, info: graphene.ResolveInfo, id_: int) -> Notebook:
        notebook = await ReadNotebook(info.context["db"]).execute(id_)
        return Notebook(
            id=notebook.id,
            title=notebook.title,
            notes=notebook.notes,
        )


class ListNotebooksQuery(graphene.ObjectType):
    all_notebooks = graphene.NonNull(graphene.List(graphene.NonNull(Notebook)))

    @staticmethod
    async def resolve_all_notebooks(parent: Any, info: graphene.ResolveInfo) -> list[Notebook]:
        return [
            Notebook(
                id=notebook.id,
                title=notebook.title,
                notes=notebook.notes,
            )
            async for notebook in ReadAllNotebook(info.context["db"]).execute()
        ]
