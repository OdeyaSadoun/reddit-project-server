from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.controllers.user_controller import register_user, get_users, get_user_from_token
from api.db.session import get_session
from api.utils.auth_bearer import JWTBearer
from api.schemas import user_schema, auth_schema
from api.models import user_model


router = APIRouter()
jwt_bearer = JWTBearer()


@router.post("/register")
def register(user: user_schema.UserCreate, session: Session = Depends(get_session)):
    return register_user(user, session)


@router.get('/getusers')
def get_users_route(jwt_token: str = Depends(jwt_bearer), session: Session = Depends(get_session)):
    return get_users(session, jwt_token)


@router.get("/get_user_info", response_model=user_schema.UserCreate)
def get_user_info(user: user_model.User = Depends(get_user_from_token)):
    return user