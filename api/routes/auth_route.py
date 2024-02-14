from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.controllers import auth_controller
from api.db.session import get_session
from api.exceptions import auth_exceptions
from api.models import jwt_bearer_model
from api.schemas import auth_schema, token_schema

router = APIRouter()
jwt_bearer = jwt_bearer_model.JWTBearer()


@router.post('/login', response_model=token_schema.TokenSchemaResponse)
def login_route(request: auth_schema.LoginSchema, db: Session = Depends(get_session)):
    try:
        return auth_controller.login(request, db)
    except auth_exceptions.IncorrectEmail:
        raise HTTPException(status_code=400, detail="Incorrect email")
    except auth_exceptions.IncorrectPassword:
        raise HTTPException(status_code=400, detail="Incorrect password")
    except auth_exceptions.JWTDecodeError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred") from e


@router.post('/logout')
def logout_route(jwt_token: str = Depends(jwt_bearer), db: Session = Depends(get_session)):
    try:
        return auth_controller.logout(jwt_token, db)
    except auth_exceptions.UnauthorizedToken:
        raise HTTPException(status_code=401, detail="Unauthorized token")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred") from e
