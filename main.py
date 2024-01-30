from model.user_model import User
from schema.user_schema import UserCreate
from db.session import engine, SessionLocal, Base
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

Base.metadata.create_all(bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app=FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World in reddit"}


@app.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(user.password)
    new_user = User(username=user.username, email=user.email, password=encrypted_password )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {new_user}