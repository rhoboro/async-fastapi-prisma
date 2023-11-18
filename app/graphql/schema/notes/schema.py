from typing import TYPE_CHECKING, Any

import graphene

from app.use_cases.notebooks import ReadNotebook

if TYPE_CHECKING:
    from ..notebooks import Notebook


class Note(graphene.ObjectType):
    id = graphene.Int(required=True)
    title = graphene.String(required=True)
    content = graphene.String(required=True)
    notebook_id = graphene.Int(required=True)
    notebook = graphene.Field("app.graphql.schema.notebooks.Notebook", required=True)

    @staticmethod
    async def resolve_notebook(parent: Any, info: graphene.ResolveInfo) -> "Notebook":
        from ..notebooks import Notebook

        notebook = getattr(parent, "notebook", None)
        if not notebook:
            notebook = await ReadNotebook(info.context["db"]).execute(parent.notebook_id)

        return Notebook(
            id=notebook.id,
            title=notebook.title,
            notes=notebook.notes,
        )
