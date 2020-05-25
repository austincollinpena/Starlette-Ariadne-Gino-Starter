from backend.utils.graphql.mutation_type import mutation
from backend.users.models import User
from backend.users.auth import verify_password, encode_auth_token
from starlette.responses import Response



@mutation.field("loginUser")
async def login_user(object, info, input):
    user = await User.query.where(User.email == input["email"]).gino.first()
    if not user:
        return {"status": "User does not exist"}
    if verify_password(input["password"], user.hashed_password):
        authToken = encode_auth_token(user.id)
        # responce = Response.set_cookie("Authentication", authToken)
        # await responce()
        return {"authToken": authToken}
    else:
        return {"message": "Incorrect password"}
