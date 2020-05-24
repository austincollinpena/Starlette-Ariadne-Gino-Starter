from ariadne import gql, MutationType, load_schema_from_path
import os

base_query_type = load_schema_from_path(
    os.path.join(os.getcwd(), "./backend/utils/graphql/query_type.graphql"))

base_mutation_type = load_schema_from_path(
    os.path.join(os.getcwd(), "./backend/utils/graphql/mutation_type.graphql"))

root_graphql_types = [base_query_type, base_mutation_type]
