from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.auth_controller import login
from schemas import TokenSchema, requestdetails
from database import get_session

router = APIRouter()

@router.post('/login', response_model=TokenSchema)
def login_route(request: requestdetails, db: Session = Depends(get_session)):
    return login(request, db)