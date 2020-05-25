# Following these docs: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

from passlib.context import CryptContext
from jwt import PyJWTError
from backend.users.models import User
from datetime import datetime, timedelta
import jwt
from backend.config import SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Create the JWT
def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        # Any time a secret is accessed from config, we need to call str() on it.
        return jwt.encode(
            payload,
            str(SECRET_KEY),
            algorithm='HS256'
        ).decode('utf-8')
    except Exception as e:
        return e


# USed to validate a token
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, str(SECRET_KEY))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


# Used during login
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Used when creating a user
def get_password_hash(password):
    return pwd_context.hash(password)
