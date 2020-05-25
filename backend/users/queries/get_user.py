from backend.utils.graphql.query_type import query
from backend.utils.decorators.check_authenticated import check_authentication
from starlette.authentication import requires


@query.field("getUser")
@check_authentication
async def resolve_get_user(user, obj, info):
    return False
