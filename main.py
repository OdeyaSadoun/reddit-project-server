from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.db.session import engine, Base
from api.routes import auth_route, users_route, reddits_route


Base.metadata.create_all(bind=engine)

app=FastAPI()

origins = [
    "http://localhost:3000", # Update this with the actual URL of your frontend application
]

# Add CORS middleware to your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Set this to True if your frontend application sends credentials (like cookies) with the requests
    allow_methods=["*"],  # Update this with the allowed HTTP methods
    allow_headers=["*"],  # Update this with the allowed request headers
)

app.include_router(users_route.router, prefix="/users", tags=["users"])
app.include_router(auth_route.router, prefix='/auth', tags=['auth'])
app.include_router(reddits_route.router, prefix='/reddits', tags=['reddits'])
