import jwt
from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.exceptions import auth_exceptions, users_exceptions
from api.models import user_model, jwt_bearer_model, token_model
from api.schemas import user_schema, auth_schema
from api.utils import jwt_utils, auth_bearer
from api.dal import auth_data_layer, users_data_layer


def register_user(user: user_schema.UserSchemaCreate):
    existing_user = auth_data_layer.get_user_by_email(user.email)
  
    if existing_user:
        raise users_exceptions.EmailAlreadyRegistered()
    print(user)
    encrypted_password = jwt_utils.get_hashed_password(user.password)
    print(encrypted_password)

    new_user = users_data_layer.create_new_user(user.name,user.email, encrypted_password)

    print(new_user)
    access = jwt_utils.create_access_token(new_user.id)
    refresh = jwt_utils.create_refresh_token(new_user.id)

    auth_data_layer.create_token(new_user.id, access, refresh)

    return {
        "access_token": access,
        "refresh_token": refresh,
    }


def get_user_from_token(token: str = Depends(jwt_bearer_model.JWTBearer()), db: Session = Depends(get_session)):

    try:
        payload = auth_bearer.decodeJWT(token)
        user_id = payload['sub']
        user = db.query(user_model.User).filter(user_model.User.id == user_id).first()

        if user is None:
            raise users_exceptions.UserNotFound()

        return user_schema.UserSchemaResponse.from_orm(user)
    
    except jwt.PyJWTError:
        raise auth_exceptions.UnauthorizedToken()
