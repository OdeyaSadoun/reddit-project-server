from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# from api.db.session import get_db
from api.controllers import reddits_controller

router = APIRouter()

# @router.post("/save_reddit_data")
# def save_reddit_data_route(reddit_data: dict, db: Session = Depends(get_db)):
#     return reddit_controller.save_reddit_data(db, reddit_data)


@router.get("/get_posts_by_subreddit")
def get_posts(subreddit: str):
    print("in route")
    return reddits_controller.get_posts_by_subreddit(subreddit)