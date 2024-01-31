from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.controllers.auth_controller import login, logout
from api.schemas import auth_schema
from api.db.session import get_session
from api.utils.auth_bearer import JWTBearer

router = APIRouter()
jwt_bearer = JWTBearer()

@router.post('/login', response_model=auth_schema.TokenSchema)
def login_route(request: auth_schema.LoginSchema, db: Session = Depends(get_session)):
    return login(request, db)

@router.post('/logout')
def logout_route(jwt_token: str = Depends(jwt_bearer), db: Session = Depends(get_session)):
    return logout(jwt_token, db)