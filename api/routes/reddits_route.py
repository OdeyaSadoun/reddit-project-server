from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from api.db.session import get_db
from api.db.session import get_session


from api.controllers import reddits_controller
from api.schemas import reddit_schema
router = APIRouter()

# @router.post("/save_reddit_data")
# def save_reddit_data_route(reddit_data: dict, db: Session = Depends(get_db)):
#     return reddit_controller.save_reddit_data(db, reddit_data)


@router.get("/get_posts_by_subreddit")
def get_posts(subreddit: str, category: str):
    print("in route")
    return reddits_controller.get_posts_from_reddit(subreddit, category)

@router.post("/redditsearches/", response_model=reddit_schema.RedditSearch)
def create_reddit_search(reddit_search: reddit_schema.RedditSearchCreate, db: Session = Depends(get_session)):
    return reddits_controller.create_reddit_search(db=db, user_id=reddit_search.user_id,reddit=reddit_search.reddit, category=reddit_search.category, search_list=reddit_search.search_list)
