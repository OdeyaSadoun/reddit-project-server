import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from pathlib import Path
from typing import Union, Any
import passlib.exc as passlib_exc
from api.exceptions import auth_exceptions


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES: int = eval(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
ALGORITHM: str = os.getenv("ALGORITHM")
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    try:
        return password_context.hash(password)
    
    except passlib_exc.PasswordHashError as e:
        raise auth_exceptions.HashingError("Error hashing password") from e


def verify_password(password: str, hashed_pass: str) -> bool:
    try:
        return password_context.verify(password, hashed_pass)
    
    except passlib_exc.PasswordHashError as e:
        raise auth_exceptions.HashingError("Error verifying password") from e
    

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    try:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
        return encoded_jwt
    
    except JWTError as e:
        raise auth_exceptions.TokenCreationError("Error creating access token") from e


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    try:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
        return encoded_jwt
    
    except JWTError as e:
        raise auth_exceptions.TokenCreationError("Error creating refresh token") from e
