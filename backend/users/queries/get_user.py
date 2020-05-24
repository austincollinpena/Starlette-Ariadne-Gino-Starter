from backend.utils.graphql.query_type import query


@query.field("getUser")
async def resolve_get_user(obj, info):
    return False
