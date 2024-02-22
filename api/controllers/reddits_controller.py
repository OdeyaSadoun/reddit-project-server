from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from api.exceptions import reddits_exceptions
from api.models import reddit_model, subreddit_model
from api.schemas import reddit_schema, subreddit_schema
from api.services.reddit import connect_reddit
from api.dal import reddits_data_layer



def get_posts_from_reddit(subreddit: str, category: str):
    posts = connect_reddit.get_posts_by_subreddit_and_category(subreddit, category)
    if (len(posts['data']['children']) <= 0):
        raise reddits_exceptions.RedditResultsNotFound("Results not found")
    return connect_reddit.get_format_posts_data(posts)


def create_reddit_search(reddit: str, category: reddit_schema.ModelRedditCategory, user_id: int):
    return reddits_data_layer.create_new_reddit_search(reddit, category, user_id)      
  

def create_subreddits_search(subreddits: list[subreddit_schema.SubredditSearchCreate]):
    return reddits_data_layer.create_new_subreddits_search(subreddits)


def get_history_searches_for_user(user_id: int):
    return reddits_data_layer.get_history_searches_for_user(user_id)


def get_history_posts_by_reddit_id(reddit_id: int):
    return reddits_data_layer.get_history_posts_by_reddit_id(reddit_id)