from typing import Any, cast

import graphene
from fastapi import APIRouter, Request

from app.database import Database

from .schema import Mutation, Query

router = APIRouter()

schema = graphene.Schema(query=Query, mutation=Mutation, subscription=None)


@router.post(
    "/graphql",
)
async def graphql(request: Request, db: Database) -> dict:
    query = cast(dict[str, Any], await request.json())
    response = await schema.execute_async(
        query.get("query", "{}"), context_value={"request": request, "db": Database}
    )
    if response.errors:
        return {"errors": [e.formatted for e in response.errors]}
    return {"data": response.data} or {"errors": [e.formatted for e in response.errors]}
