from backend.utils.graphql.query_type import query
from backend.utils.decorators.check_authenticated import check_authentication
from starlette.authentication import requires
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse


@query.field("getUser")
@check_authentication
async def resolve_get_user(user, obj, info):
    
    tasks = BackgroundTasks()
    tasks.add_task(testFunc)
    return False


async def testFunc():
    print('I did it!')
