from ariadne import gql

from ariadne import QueryType, make_executable_schema, ObjectType, snake_case_fallback_resolvers, load_schema_from_path
from ariadne.asgi import GraphQL
from starlette.applications import Starlette

from ariadne import MutationType
from backend import auth_mutation
from backend.howto.multi_file_mutation.functions import make_mutation

# For debugging:
import uvicorn
import os

# uvicorn backend.main:app

# Define the type definitions
from backend.howto.multi_file_mutation.main import make_mutation_parent

type_defstwo = gql("""
    type Query {
        hello: String!
        user: User
        holidays(year: Int): [String]!
        client: Client
    }
    type User {
       username: String! 
       email: String!
       firstName: String!
       lastName: String!
    }
    type Client {
        email: String!
    }
""")

type_defs = load_schema_from_path("./backend/.graphql")

# Create a querytype instance for the query defined in our schema
query = QueryType()
mutation = MutationType()
mutation.set_field("login", auth_mutation.resolve_login)
mutation.set_field("logout", auth_mutation.resolve_logout)
mutation.set_field("test", make_mutation)


@query.field("holidays")
def resolve_holidays(*_, year=None):
    if year:
        return ["what I would get if there was a year passed through"]
    return ["what I would get if there was no year passed through"]


# When you're looking for the query "hello," as defined in our typedefs
@query.field("hello")
def resolve_hello(_, info):  # Resolve that hello
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")
    return f"Hello {user_agent}"


@query.field("user")
def resolve_user(_, info):
    a = 1
    a
    return {"first_name": "Austin", "last_name": "Pena"}


# Need to define the object first
user = ObjectType("User")


@user.field("username")
def resolve_username(obj, info, *_):
    a = 1
    a
    return f'{obj["first_name"]} {obj["last_name"]}'


client = ObjectType("Client")


@user.field("email")
@client.field("email")
def resolve_email(obj, info):
    return "email"


@query.field("client")
def resolve_client(obj, info):
    return "client"


schema = make_executable_schema(type_defs, mutation, query, user, client,
                                snake_case_fallback_resolvers)

# Create executable schema instance

# In the future we'll look more like this
# make_executable_schema(type_defs, [query, user, mutations, fallback_resolvers])

# Make the graphql server
graphql_server = GraphQL(schema)

app = Starlette(debug=True)
app.mount("/graphql", GraphQL(schema, debug=True))

# For debugging
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

# TODO

# Multipe file support?

# from .resolvers import resolve_email_with_permission_check
#
# user = ObjectType("User")
# user.set_field("email", resolve_email_with_permission_check)


# Other resources
# https://perandrestromhaug.com/posts/guide-to-schema-first-graphql-with-django-and-ariadne/
