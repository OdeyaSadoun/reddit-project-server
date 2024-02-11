from fastapi import APIRouter, Depends, HTTPException, security
from sqlalchemy.orm import Session
# from api.db.session import get_db
from api.db.session import get_session
from typing import List


from api.controllers import reddits_controller
from api.schemas import reddit_schema, subreddit_schema
from api.utils import auth_bearer
from api.models import jwt_bearer_model
router = APIRouter()

# @router.post("/save_reddit_data")
# def save_reddit_data_route(reddit_data: dict, db: Session = Depends(get_db)):
#     return reddit_controller.save_reddit_data(db, reddit_data)


@router.get("/get_posts_by_subreddit")
def get_posts(subreddit: str, category: str):
    print("in route")
    return reddits_controller.get_posts_from_reddit(subreddit, category)


@router.post("/redditsearches")
def create_reddit_search(reddit_search: reddit_schema.RedditSearchCreate, db: Session = Depends(get_session)):
    print("enter route")
    return reddits_controller.create_reddit_search(db, reddit_search.reddit, reddit_search.category, reddit_search.user_id)



@router.post("/subredditsearches")
def create_subreddit_search(subreddit_search: List[subreddit_schema.SubredditSearchCreate], db: Session = Depends(get_session)):
    print("enter route subreddit")
    return reddits_controller.create_subreddits_search(db, subreddit_search)


@router.get("/")
def get_history():
    print('**************')
    # return reddits_controller.get_recent_searches_for_user(db)
    return {"message" : "aaaaa"}

jwt_bearer = jwt_bearer_model.JWTBearer()

@router.get("/recent")
def get_recent_searches(db: Session = Depends(get_session),jwt_token: str = Depends(jwt_bearer)):
    payload = auth_bearer.decodeJWT(jwt_token)
    user_id = payload['sub']

    # user_id = int(user_id)
    print(user_id)
    return reddits_controller.get_recent_searches_for_user(db,user_id)


@router.get("/history/{reddit_id}")
def get_recent_searches_for_user(reddit_id: int, db: Session = Depends(get_session)):
    return reddits_controller.get_history_posts_by_reddit_id(db, reddit_id)