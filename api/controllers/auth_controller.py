from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status, security
from functools import wraps
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from api.models import user_model, token_model
from api.schemas import auth_schema
from api.utils import auth_bearer, jwt_utils



oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")


def some_protected_endpoint(token: str = Depends(oauth2_scheme)):
    return {"token": token}


def login(request: auth_schema.LoginSchema, session: Session):
    user = session.query(user_model.User).filter(user_model.User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not jwt_utils.verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    access = jwt_utils.create_access_token(user.id)
    refresh = jwt_utils.create_refresh_token(user.id)

    token_db = token_model.TokenTable(user_id=user.id, access_token=access, refresh_token=refresh, status=True)
    session.add(token_db)
    session.commit()
    session.refresh(token_db)
    
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


def logout(jwt_token: str, db: Session):
    payload = auth_bearer.decodeJWT(jwt_token)
    user_id = payload['sub']

    now_utc = datetime.now(timezone.utc)  # Get UTC time

    token_records = db.query(token_model.TokenTable).filter(token_model.TokenTable.user_id == user_id).all()

    for record in token_records:
        record.created_date = record.created_date.replace(tzinfo=timezone.utc)

        if (now_utc - record.created_date).days > 1:
            db.delete(record)

    existing_token = db.query(token_model.TokenTable).filter(token_model.TokenTable.user_id == user_id, token_model.TokenTable.access_token == jwt_token).first()

    if existing_token:
        existing_token.status = False
        db.commit()
        db.refresh(existing_token)

    return {"message": "Logout Successfully"}


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            payload = auth_bearer.decodeJWT(kwargs['dependencies'])
            user_id = payload['sub']
            data = kwargs['session'].query(token_model.TokenTable).filter_by(user_id=user_id, access_token=kwargs['dependencies'], status=True).first()
            if data:
                return func(kwargs['dependencies'], kwargs['session'])
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token blocked")
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
    return wrapper