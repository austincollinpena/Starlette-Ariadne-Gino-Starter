from backend.utils.graphql.mutation_type import mutation


@mutation.field("createUser")
def create_user(object, info, input):
    return {"email": "austincollin", "password": "Austin's PAssword"}
