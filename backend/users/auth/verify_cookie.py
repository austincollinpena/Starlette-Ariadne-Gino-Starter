from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
from . import decode_auth_token
from backend.users.models import User


class VerifyCookie(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return UnauthenticatedUser
        auth = request.headers["Authorization"]
        type = auth.split()[0]
        if type is not "Bearer":
            return UnauthenticatedUser
        # Get the user's id
        try:
            token_sub = decode_auth_token(auth.split()[1])
            return SimpleUser(User.get(token_sub).email)
        except:
            return AuthenticationError

        return SimpleUser()
