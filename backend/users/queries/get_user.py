import asyncio
import time

from starlette.background import BackgroundTasks

from backend.utils.graphql.query_type import query
from backend.utils.decorators.check_authenticated import check_authentication


@query.field("getUser")
@check_authentication
async def resolve_get_user(user, obj, info):
    task = await BackgroundTasks()
    task.add_task(test_func)
    task.add_task(testing_func_two, "I work now")
    request = info.context["request"]
    request.state.background = task
    return True


async def test_func():
    await asyncio.sleep(10)
    print("once!!")


async def testing_func_two(message: str):
    print(message)
