from sqlalchemy.orm import Session

from api.models import reddit_model, subreddit_model
from api.schemas import reddit_schema, subreddit_schema
from api.services.reddit import connect_reddit


def get_posts_from_reddit(subreddit: str, category: str):
    posts = connect_reddit.get_posts_by_subreddit_and_category(subreddit, category)
    return connect_reddit.get_format_posts_data(posts)


def create_reddit_search(db: Session, reddit: str, category: reddit_schema.ModelRedditCategory, user_id: int):
    db_reddit_search = reddit_model.RedditSearch(user_id=user_id, reddit=reddit, category=category)
    db.add(db_reddit_search)
    db.commit()
    db.refresh(db_reddit_search)
    return db_reddit_search


def create_subreddits_search(db: Session, subreddits: list[subreddit_schema.SubredditSearchCreate]):
    db_subreddits_search = []
    for subreddit in subreddits:
        db_subreddit_search = subreddit_model.SubredditSearch(reddit_id=subreddit.reddit_id, title=subreddit.title, selftext=subreddit.selftext, sentiment=subreddit.sentiment, ups=subreddit.ups, downs=subreddit.downs, score=subreddit.score)
        db.add(db_subreddit_search)
        db.commit()
        db.refresh(db_subreddit_search)
        db_subreddits_search.append(db_subreddit_search)
    
    return db_subreddits_search


def get_history_searches_for_user(db: Session, user_id: int):
    return db.query(reddit_model.RedditSearch).filter(reddit_model.RedditSearch.user_id == user_id).all()


def get_history_posts_by_reddit_id(db: Session, reddit_id: int):
    return db.query(subreddit_model.SubredditSearch).filter(subreddit_model.SubredditSearch.reddit_id == reddit_id).all()