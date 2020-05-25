from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
from . import decode_auth_token
from backend.users.models import User


class VerifyCookie(AuthenticationBackend):
    async def authenticate(self, request):
        if "authorization" not in request.headers:
            return
        auth = request.headers["authorization"]
        type = auth.split()[0]
        if type != "Bearer":
            return UnauthenticatedUser()
        # Get the user's id from the JWT
        try:
            token_sub = decode_auth_token(auth.split()[1])
            return [AuthCredentials(["authenticated"]), SimpleUser(token_sub)]
        except:
            return
