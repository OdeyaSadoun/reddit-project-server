from fastapi import FastAPI

from api.db.session import engine, Base
from api.routes import auth_route, users_route


Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(users_route.router, prefix="/users", tags=["users"])
app.include_router(auth_route.router, prefix='/auth', tags=['auth'])
