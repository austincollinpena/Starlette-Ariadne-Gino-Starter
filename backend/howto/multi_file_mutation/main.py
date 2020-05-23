# Keep in mind that ariadne always requires a query at least somewhere
from ariadne import gql, MutationType
from backend.howto.multi_file_mutation.functions import make_mutation as yeet


# 1. A simple mutation:
# Define your mutation schema:

# type Mutation{
#     testOne(argOne: String!): TestPayload
# }

# Add your resolver function TAKING IN the arg
async def test_one_function(_, info, argOne):
    if argOne == "condition":
        return True
    return False


# Define your TYPE MUTATION class
make_mutation_parent = MutationType()
# Connect that the class of this mutation has the field and resolver you want
make_mutation_parent.set_field("testOne", test_one_function)


# IT works!

# 2. Working with additional input types
# Here we can see that sampleTwo takes in a custom defined input, and test spits out a custom payload
# type Mutation{
#     test(argOne: String!): TestPayload
#     testOne(argOne: String!): Boolean
#     sampleTwo(input: TestInput): Boolean!
# }
#
# input TestInput{
#     isCool: Boolean
#     isGay: Boolean
# }
#
# type TestPayload{
#     success: Boolean
#     message: String
# }

# To manage this, all you need to do for test is return a dict with {success: True, message: "message"}

# for sampleTwo however, the input is actually a dict!
def sample_two_function(_, info, input):
    if input["isCool"] is True:
        return True
