from fastapi import Depends, security
from functools import wraps
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from api.dal import auth_data_layer, users_data_layer
from api.exceptions import auth_exceptions
from api.models import token_model
from api.schemas import auth_schema
from api.utils import auth_bearer, jwt_utils

oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")


def some_protected_endpoint(token: str = Depends(oauth2_scheme)):
    return {"token": token}


def login(request: auth_schema.LoginSchema):
    user = users_data_layer.get_user_by_email(request.email)
    if user is None:
        raise auth_exceptions.IncorrectEmail()
    
    hashed_pass = user.password
    if not jwt_utils.verify_password(request.password, hashed_pass):
        raise auth_exceptions.IncorrectPassword()

    access = jwt_utils.create_access_token(user.id)
    refresh = jwt_utils.create_refresh_token(user.id)

    auth_data_layer.create_token(user.id, access, refresh)

    return {
        "access_token": access,
        "refresh_token": refresh,
    }



def logout(jwt_token: str, db: Session):
    payload = auth_bearer.decodeJWT(jwt_token)
    user_id = payload['sub']

    auth_data_layer.delete_expired_tokens(user_id)

    auth_data_layer.deactivate_token(user_id)

    return {"message": "Logout Successfully"}


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            payload = auth_bearer.decodeJWT(kwargs['dependencies'])
            user_id = payload['sub']
            data = kwargs['session'].query(token_model.TokenTable).filter_by(user_id=user_id,
                                                                             access_token=kwargs['dependencies'],
                                                                             status=True).first()
            if data:
                return func(kwargs['dependencies'], kwargs['session'])
            else:
                raise auth_exceptions.TokenBlocked()
        except InvalidTokenError:
            raise auth_exceptions.InvalidToken()
    return wrapper