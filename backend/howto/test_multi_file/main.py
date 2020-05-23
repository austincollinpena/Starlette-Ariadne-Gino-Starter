from ariadne import gql, MutationType, load_schema_from_path
import os

from pathlib import Path


def sample_function(_, info):
    return True


# Define your TYPE MUTATION class
make_mutation_parent = MutationType()
# Connect that the class of this mutation has the field and resolver you want
make_mutation_parent.set_field("testOne", sample_function)

test_type_defs = load_schema_from_path(
    os.path.join(os.getcwd(), "./backend/howto/test_multi_file/test_sample_mutation.graphql"))
