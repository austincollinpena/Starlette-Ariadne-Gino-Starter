from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from ariadne.contrib.tracing.apollotracing import ApolloTracingExtension

from backend.db.main import db as gino_db

# For debugging:
import uvicorn

from backend.users.queries import get_user_type_defs
from backend.utils.graphql.query_type import query as root_query
from backend.utils.graphql import root_graphql_types

schema = make_executable_schema([*root_graphql_types, get_user_type_defs], root_query)

app = Starlette(debug=True)
gino_db.init_app(app)

app.mount("/graphql", GraphQL(schema, debug=True, extensions=[ApolloTracingExtension]))

# For debugging
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

# TODO: Auth
# https://spectrum.chat/ariadne/general/how-to-implement-a-very-simple-auth-layer~80b7d221-6d0c-4df8-800a-e4cc6a07c99d
