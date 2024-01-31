import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.db.session import get_session

from api.models import user_model
from api.schemas import user_schema, auth_schema
from api.utils import jwt_utils, auth_bearer

# from utils import verify_password, get_hashed_password


def register_user(user: user_schema.UserCreate, session: Session):
    existing_user = session.query(user_model.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = jwt_utils.get_hashed_password(user.password)
    new_user = user_model.User(username=user.username, email=user.email, password=encrypted_password)

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
        users = session.query(user_model.User).all()
        return users
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token.")


def change_password(request: auth_schema.ChangePassword, db: Session):
    user = db.query(user_model.User).filter(user_model.User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not auth_bearer.verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    encrypted_password = auth_bearer.get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()

    return {"message": "Password changed successfully"}


def get_user_from_token(token: str = Depends(auth_bearer.JWTBearer()), db: Session = Depends(get_session)):

    try:
        payload = auth_bearer.decodeJWT(token)
        user_id = payload['sub']
        user = db.query(user_model.User).filter(user_model.User.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
    except auth_bearer.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
