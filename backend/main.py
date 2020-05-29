from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.middleware import Middleware
from ariadne.contrib.tracing.apollotracing import ApolloTracingExtension

# Local Packages
from backend.db import db as gino_db

# For debugging:
import uvicorn

# Type defs
from backend.users.queries import user_query_schema
from backend.utils.graphql.query_type import query as root_query
from backend.utils.graphql.mutation_type import mutation as root_mutation
from backend.utils.graphql import root_graphql_types
from backend.users import user_type_defs

schema = make_executable_schema(
    [*root_graphql_types, *user_type_defs], root_query, root_mutation)

from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class BackgroundTaskMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Available as info.context["request"].state.background
        request.state.background = BackgroundTask()
        response = await call_next(request)
        response.background = request.state.background
        return response


middleware = [
    Middleware(BackgroundTaskMiddleware)
]

app = Starlette(debug=True, middleware=middleware)
gino_db.init_app(app)
# load_modules(app)
app.mount("/graphql", GraphQL(schema, debug=True,
                              extensions=[ApolloTracingExtension]))

# For debugging
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

# TODO: Auth
# https://spectrum.chat/ariadne/general/how-to-implement-a-very-simple-auth-layer~80b7d221-6d0c-4df8-800a-e4cc6a07c99d
# Session middlewere

# TODO: CORS middleware and more
