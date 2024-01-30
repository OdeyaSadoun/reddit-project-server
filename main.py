from fastapi import FastAPI

from api.db.session import engine, Base
from api.routes import user_route


Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(user_route.router, prefix="/user", tags=["users"])