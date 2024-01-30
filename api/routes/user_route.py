from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.schemas.user_schema import UserCreate
from api.controllers.user_controller import register_user, get_users
from api.db.session import get_session
from api.utils.jwt_utils import JWTBearer

router = APIRouter()
jwt_bearer = JWTBearer()


@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    return register_user(user, session)


@router.get('/getusers')
def get_users_route(jwt_token: str = Depends(jwt_bearer), session: Session = Depends(get_session)):
    return get_users(session, jwt_token)