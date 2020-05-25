from starlette.authentication import (AuthenticationError)
from backend.users.auth import decode_auth_token


def check_authentication(func):
    def wrapper(obj, info, **kwargs):
        request = info.context["request"]
        jwt = request.headers.get("authorization")
        type = jwt.split()[0]
        if type != "Bearer":
            raise AuthenticationError
        # Get the user's id from the JWT
        try:
            token_sub = decode_auth_token(jwt.split()[1])
            return func(token_sub, obj, info, **kwargs)
        except:
            raise AuthenticationError

    return wrapper
