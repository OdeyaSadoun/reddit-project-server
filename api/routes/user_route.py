from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.controllers import user_controller
from api.db.session import get_session
from api.models import user_model
from api.schemas import user_schema
from api.utils import auth_bearer


router = APIRouter()
jwt_bearer = auth_bearer.JWTBearer()


@router.post("/register")
def register(user: user_schema.UserSchemaCreate, session: Session = Depends(get_session)):
    return user_controller.register_user(user, session)


@router.get('/getusers')
def get_users_route(jwt_token: str = Depends(jwt_bearer), session: Session = Depends(get_session)):
    return user_controller.get_users(session, jwt_token)


@router.get("/get_user_info", response_model=user_schema.UserSchemaResponse)
def get_user_info(user: user_model.User = Depends(user_controller.get_user_from_token)):
    return user