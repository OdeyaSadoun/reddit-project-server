from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.db.session import engine, Base
from api.routes import auth_route, users_route, reddits_route
from api.db.session import get_session


Base.metadata.create_all(bind=engine)

app=FastAPI()

origins = [
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(users_route.router, prefix="/users", tags=["users"])
app.include_router(auth_route.router, prefix='/auth', tags=['auth'])
app.include_router(reddits_route.router, prefix='/reddits', tags=['reddits'])
