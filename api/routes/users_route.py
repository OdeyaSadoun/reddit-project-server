from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.controllers import users_controller
from api.db.session import get_session
from api.models import user_model, jwt_bearer_model
from api.schemas import user_schema


router = APIRouter()
jwt_bearer = jwt_bearer_model.JWTBearer()


@router.post("/register")
def register(user: user_schema.UserSchemaCreate, session: Session = Depends(get_session)):
    return users_controller.register_user(user, session)


@router.get('/getusers')
def get_users_route(jwt_token: str = Depends(jwt_bearer), session: Session = Depends(get_session)):
    return users_controller.get_users(session, jwt_token)


@router.get("/get_user_info", response_model=user_schema.UserSchemaResponse)
def get_user_info(user: user_model.User = Depends(users_controller.get_user_from_token)):
    return user