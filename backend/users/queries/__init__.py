# Import the Graphql files and put them in a list
import os

from ariadne import load_schema_from_path


get_user_type_defs = load_schema_from_path(
    os.path.join(os.getcwd(), "backend", "users", "queries"))

user_queries = [
    get_user_type_defs,
]
