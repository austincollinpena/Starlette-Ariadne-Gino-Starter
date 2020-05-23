from ariadne import gql

from ariadne import QueryType, make_executable_schema, ObjectType

# Step one: in your type def, add the argument
type_def = """
    type Query {
        holidays(year: Int): [String]!
    }
"""

query = QueryType()

@query.field("holidays")
def resolve_holidays(*_, year=None):
    if year:
        return "what I would get if there was a year passed through"
    return "what I would get if there was no year passed through"
