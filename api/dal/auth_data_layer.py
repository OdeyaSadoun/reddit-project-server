from datetime import datetime, timezone
from api.models import token_model
from api.db.session import db
from api.exceptions import auth_exceptions
from sqlalchemy.exc import SQLAlchemyError


def create_token(user_id: int, access_token: str, refresh_token: str) -> token_model.TokenTable:
    try:
        new_token = token_model.TokenTable(user_id=user_id, access_token=access_token, refresh_token=refresh_token, status=True)
        db.add(new_token)
        db.commit()
        db.refresh(new_token)
        print(new_token)
        return new_token
    except SQLAlchemyError as e:
        raise auth_exceptions.TokenCreationError(str(e))


def delete_expired_tokens(user_id: int):
    try:
        now_utc = datetime.now(timezone.utc) 
        token_records = db.query(token_model.TokenTable).filter(token_model.TokenTable.user_id == user_id).all()
        for record in token_records:
            record.created_date = record.created_date.replace(tzinfo=timezone.utc)
            if (now_utc - record.created_date).days > 1:
                db.delete(record)
        db.commit()
    except SQLAlchemyError as e: 
        raise auth_exceptions.DeleteTokenExpiredError(str(e))


def deactivate_token(user_id: int):
    try:
        existing_token = db.query(token_model.TokenTable).filter(token_model.TokenTable.user_id == user_id).first()
        if existing_token:
            existing_token.status = False
            db.commit()
            db.refresh(existing_token)
    except SQLAlchemyError as e:  
        raise auth_exceptions.DeactivateTokenExpiredError(str(e))



