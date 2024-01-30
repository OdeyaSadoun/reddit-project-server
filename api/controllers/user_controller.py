from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api.models.user_model import User
from api.schemas import user_schema, auth_schema
from api.utils import jwt_utils, auth_bearer

# from utils import verify_password, get_hashed_password


def register_user(user: user_schema.UserCreate, session: Session):
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
        payload = jwt_utils.decodeJWT(jwt_token)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token.")
    
    if payload:
        users = session.query(User).all()
        return users
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token.")


def change_password(request: auth_schema.changepassword, db: Session):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not auth_bearer.verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    encrypted_password = auth_bearer.get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()

    return {"message": "Password changed successfully"}