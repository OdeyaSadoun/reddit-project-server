from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api.models.user_model import User
from api.schemas.user_schema import UserCreate
from api.utils import jwt_utils
from api.utils.jwt_utils import decodeJWT


def register_user(user: UserCreate, session: Session):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = jwt_utils.get_hashed_password(user.password)
    new_user = User(username=user.username, email=user.email, password=encrypted_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "user created successfully", "user": new_user}


def get_users(session: Session, jwt_token: str):
    # Add any additional logic for user retrieval or validation based on the token
    try:
        payload = decodeJWT(jwt_token)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token.")
    
    if payload:
        users = session.query(User).all()
        return users
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token.")
