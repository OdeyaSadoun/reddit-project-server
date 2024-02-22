from api.models import user_model
from api.db.session import db
from sqlalchemy.exc import SQLAlchemyError
from api.exceptions import users_exceptions


def create_new_user(name: str, email: str, encrypted_password: str) -> user_model.User:
    try:
        print("in")
        new_user = user_model.User(name=name, email=email, password=encrypted_password)
        print(new_user)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        raise users_exceptions.CreateUserError(str(e))