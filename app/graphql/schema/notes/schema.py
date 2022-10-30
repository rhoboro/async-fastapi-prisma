from typing import TYPE_CHECKING, Any

import graphene

from app import models

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
            notebook = await models.Notebook.read_by_id(
                parent.notebook_id,
                include_notes=True,
            )

        return Notebook(
            id=notebook.id,
            title=notebook.title,
            notes=notebook.notes,
        )
