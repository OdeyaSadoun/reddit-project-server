import jwt
from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.exceptions import auth_exceptions, users_exceptions
from api.models import user_model, jwt_bearer_model,token_model
from api.schemas import user_schema, auth_schema
from api.utils import jwt_utils, auth_bearer


def register_user(user: user_schema.UserSchemaCreate, db: Session):
    existing_user = db.query(user_model.User).filter_by(email=user.email).first()
    if existing_user:
        raise users_exceptions.EmailAlreadyRegistered()
    
    encrypted_password = jwt_utils.get_hashed_password(user.password)
    new_user = user_model.User(name=user.name, email=user.email, password=encrypted_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access = jwt_utils.create_access_token(new_user.id)
    refresh = jwt_utils.create_refresh_token(new_user.id)

    new_token = token_model.TokenTable(user_id=new_user.id, access_token=access, refresh_token=refresh, status=True)
    db.add(new_token)
    db.commit()
    db.refresh(new_token)

    return {
        "access_token": access,
        "refresh_token": refresh,
    }


def change_password(request: auth_schema.ChangePasswordSchema, db: Session):
    user = db.query(user_model.User).filter(user_model.User.email == request.email).first()
    if user is None:
        raise users_exceptions.UserNotFound()
    
    if not jwt_utils.verify_password(request.old_password, user.password):
        raise users_exceptions.InvalidOldPassword()

    encrypted_password = jwt_utils.get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()

    return {"message": "Password changed successfully"}


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
