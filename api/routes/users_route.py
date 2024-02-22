from fastapi import APIRouter, Depends, HTTPException

from api.controllers import users_controller
from api.exceptions import users_exceptions, auth_exceptions
from api.models import user_model, jwt_bearer_model
from api.schemas import user_schema

router = APIRouter()
jwt_bearer = jwt_bearer_model.JWTBearer()


@router.post("/register")
def register(user: user_schema.UserSchemaCreate):
    try:
        return users_controller.register_user(user)
    
    except users_exceptions.EmailAlreadyRegistered:
        raise HTTPException(status_code=400, detail="Email already registered")
    except users_exceptions.CreateUserError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred") from e


@router.get("/userinfo", response_model=user_schema.UserSchemaResponse)
def get_user_info(user: user_model.User = Depends(users_controller.get_user_from_token)):
    try:
        return user
    
    except users_exceptions.UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
    except auth_exceptions.UnauthorizedToken:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred") from e
