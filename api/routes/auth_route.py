from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.controllers import auth_controller
from api.db.session import get_session
from api.models import jwt_bearer_model
from api.schemas import auth_schema, token_schema

router = APIRouter()
jwt_bearer = jwt_bearer_model.JWTBearer()


@router.post('/login', response_model=token_schema.TokenSchemaResponse)
def login_route(request: auth_schema.LoginSchema, db: Session = Depends(get_session)):
    return auth_controller.login(request, db)


@router.post('/logout')
def logout_route(jwt_token: str = Depends(jwt_bearer), db: Session = Depends(get_session)):
    return auth_controller.logout(jwt_token, db)