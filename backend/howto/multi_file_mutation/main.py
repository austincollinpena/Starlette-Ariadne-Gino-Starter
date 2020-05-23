# Keep in mind that ariadne always requires a query at least somewhere
from ariadne import gql, MutationType
from backend.howto.multi_file_mutation.functions import make_mutation as yeet

# Step one, define the mutation in your schema
# sample_type_defs = gql("""
#     type Mutation{
#         make_mutation(arg1: String!, arg2: Boolean!)
#     }
# """)

# Step two, tell ariadne what the mutation is
make_mutation_parent = MutationType()
make_mutation_parent.set_field("test", yeet)
