from ariadne import gql

from ariadne import QueryType, make_executable_schema, ObjectType, snake_case_fallback_resolvers
from ariadne.asgi import GraphQL
from starlette.applications import Starlette

# There are three steps to making a query
# 1. Add your object to the query and typedef. This makes it "queryable" and shows the response type

type_defs = gql("""
    type Query {
        user: User
    }
    type User {
        firstname: String!
        lastName: String!
       username: String! 
       email: String!
    }
""")

# 2. make a querytype instance

# Create a querytype instance for the query defined in our schema
query = QueryType()


# 3. Write your query resolver. When you look for the QUERY of USER, what do you get?
# Important! Now when I query user{firstName}, I get Austin :)
@query.field("user")
def resolve_user(obj, info):
    return {"first_name": "Austin", "last_name": "Pena"}


# 4. Define what the "user" actually is
user = ObjectType("User")


# 5. Register the CALCULATED
# Because this is a USER field, it inherits the object of the user
@user.field("username")
def resolve_username(obj, info):
    return obj["first_name"] + obj["last_name"]


# Make the executable schema
schema = make_executable_schema(type_defs, query, user, snake_case_fallback_resolvers)
