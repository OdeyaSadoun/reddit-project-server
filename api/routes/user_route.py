from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.schemas.user_schema import UserCreate
from api.controllers.user_controller import register_user
from api.db.session import get_session

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    return register_user(user, session)