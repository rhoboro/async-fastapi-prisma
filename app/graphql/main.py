from typing import Any, Union, cast

import graphene
from fastapi import APIRouter, Request

from .schema import Mutation, Query

router = APIRouter()

schema = graphene.Schema(query=Query, mutation=Mutation, subscription=None)


@router.post(
    "/graphql",
)
async def graphql(request: Request):
    query = cast(Union[dict[str, Any], list[Any]], await request.json())
    response = await schema.execute_async(
        query.get("query", "{}"), context_value={"request": request}
    )
    if response.errors:
        return {"errors": [e.formatted for e in response.errors]}
    return response.data or {"errors": [e.formatted for e in response.errors]}
