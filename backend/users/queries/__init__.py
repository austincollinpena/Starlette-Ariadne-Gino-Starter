# Import the Graphql files and put them in a list
import os

from ariadne import load_schema_from_path

from os.path import dirname, basename, isfile, join
import glob

# Make all the resolvers available via the package
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

from backend.users.queries import *

get_user_type_defs = load_schema_from_path(
    os.path.join(os.getcwd(), "backend", "users", "queries"))

user_queries = [
    get_user_type_defs,
]
