from api.models import reddit_model, subreddit_model
from api.db.session import db
from sqlalchemy.exc import SQLAlchemyError
from api.exceptions import reddits_exceptions
from api.schemas import reddit_schema, subreddit_schema
from pydantic import ValidationError


def create_new_reddit_search(reddit: str, category: reddit_schema.ModelRedditCategory, user_id: int) -> reddit_model.RedditSearch:
    try:
        new_search = reddit_model.RedditSearch(reddit=reddit, category=category, user_id=user_id)
        db.add(new_search)
        db.commit()
        db.refresh(new_search)
        return new_search
    except SQLAlchemyError as e:
        raise reddits_exceptions.RedditDatabaseAccessError("Error accessing the database") from e
    except ValidationError as e:
        raise reddits_exceptions.RedditValidationError("Invalid parameters provided") from e
    

def create_new_subreddits_search(subreddits: list[subreddit_schema.SubredditSearchCreate]):
    db_subreddits_search = []
    try:
        for subreddit in subreddits:
            db_subreddit_search = subreddit_model.SubredditSearch(reddit_id=subreddit.reddit_id, title=subreddit.title, selftext=subreddit.selftext, sentiment=subreddit.sentiment, ups=subreddit.ups, downs=subreddit.downs, score=subreddit.score)
            db.add(db_subreddit_search)
            db.commit()
            db.refresh(db_subreddit_search)
            db_subreddits_search.append(db_subreddit_search)
        
        return db_subreddits_search
    except SQLAlchemyError as e:
        raise reddits_exceptions.RedditDatabaseAccessError("Error accessing the database") from e
    except ValidationError as e:
        raise reddits_exceptions.RedditValidationError("Invalid parameters provided") from e


def get_history_searches_for_user(user_id: int):
    try:
        return db.query(reddit_model.RedditSearch).filter(reddit_model.RedditSearch.user_id == user_id).all()
    except SQLAlchemyError as e:
        raise reddits_exceptions.RedditDatabaseAccessError("Error accessing the database") from e


def get_history_posts_by_reddit_id(reddit_id: int):
    try:
        return db.query(subreddit_model.SubredditSearch).filter(subreddit_model.SubredditSearch.reddit_id == reddit_id).all()
    except SQLAlchemyError as e:
        raise reddits_exceptions.RedditDatabaseAccessError("Error accessing the database") from e
    