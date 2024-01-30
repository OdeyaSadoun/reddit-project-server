from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.models.user_model import User
from api.schemas.user_schema import UserCreate
from api.utils import jwt_util

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_hashed_password(password: str) -> str:
#     return pwd_context.hash(password)


def register_user(user: UserCreate, session: Session):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = jwt_util.get_hashed_password(user.password)
    new_user = User(username=user.username, email=user.email, password=encrypted_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "user created successfully", "user": new_user}
