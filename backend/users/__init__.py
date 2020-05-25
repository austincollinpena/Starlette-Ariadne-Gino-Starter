from .queries import user_query_schema
from .types import user_type_schema
from .mutations import user_mutation_schema

user_type_defs = [user_query_schema, user_type_schema, user_mutation_schema]
