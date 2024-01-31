from fastapi import FastAPI

from api.db.session import engine, Base
from api.routes import user_route, auth_route


Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(user_route.router, prefix="/users", tags=["users"])
app.include_router(auth_route.router, prefix='/auth', tags=['auth'])
