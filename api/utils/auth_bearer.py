import os
from dotenv import load_dotenv
import jwt
from pathlib import Path

from api.models import jwt_bearer_model

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES: int = eval(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
ALGORITHM: str = os.getenv("ALGORITHM")
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY")


def decodeJWT(jwtoken: str):
    try:
        # Decode and verify the token
        payload = jwt.decode(jwtoken, JWT_SECRET_KEY, ALGORITHM)
        return payload
    except jwt.PyJWTError:
        return None


jwt_bearer = jwt_bearer_model.JWTBearer()
