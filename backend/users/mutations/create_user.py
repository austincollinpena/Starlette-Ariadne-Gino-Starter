from backend.utils.graphql.mutation_type import mutation
from backend.users.models import User, Profile
from backend.users.auth import encode_auth_token, get_password_hash
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse


@mutation.field("createUser")
async def create_user(object, info, input):
    # Check if the user exists
    user = await User.query.where(User.email == input["email"]).gino.first()
    task = BackgroundTask(sample_background)
    if user:
        return {"status": "This user already exists, please log in"}
    if user is None:
        user = await User.create(email=input["email"], hashed_password=get_password_hash(input["password"]))
        authToken = encode_auth_token(user.id)
        return {"email": input["email"], "status": "User created",
                "authToken": authToken}


async def sample_background():
    print('IM BACKGROUND')
    return


async def create_profile(user_id):
    print('IM CREATING A PROFILE')
    profile = await Profile.create(user_id=user_id)
    return
