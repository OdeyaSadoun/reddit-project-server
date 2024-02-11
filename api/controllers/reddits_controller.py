from sqlalchemy.orm import Session
from api.models import reddit_model, subreddit_model
from fastapi import HTTPException
from typing import List

from api.models import reddit_model, subreddit_model
from api.schemas import reddit_schema, subreddit_schema

import os
from dotenv import load_dotenv
from pathlib import Path
import requests
from fastapi import Depends, HTTPException

from api.services.sentiment_analysis import sentiments_model

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = get_user(token)
#     if user is None:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return user


def save_reddit_data(db: Session, reddit_data: dict):
    try:
        # Create an instance of the RedditSearch model
        reddit_search_instance = reddit_model.RedditSearch(**reddit_data)

        # Add the instance to the session
        db.add(reddit_search_instance)

        # Commit the changes to the database
        db.commit()

        return {"message": "Data saved successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")


def get_headers_from_connection_to_reddit_by_access_token():
    client_id: str = os.getenv('REDDIT_CLIENT_ID')
    secret_key: str = os.getenv('REDDIT_SECRET_KEY')
    username: str = os.getenv('REDDIT_USERNAME')
    password: str = os.getenv('REDDIT_PASSWORD')

    auth = requests.auth.HTTPBasicAuth(client_id, secret_key)
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }
    headers = {'User-Agent': 'MyApi/0.0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers, params={'limit': '100', 'after': 't3_1ae05y3'})
    token = res.json()['access_token']
    headers = {**headers, **{'Authorization': f'bearer {token}'}}

    return headers


def get_posts_by_subreddit(subreddit: str):
    print("in func1")
    # for default get the new posts, default amount = 25
    return get_posts_by_subreddit_and_category(subreddit=subreddit, category="new")


def get_posts_by_subreddit_and_category(subreddit: str, category: str):
    print("in func2")
    headers = get_headers_from_connection_to_reddit_by_access_token()
    res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/{category}', headers=headers, params={'limit':'10'})
    return res.json()


def get_format_posts_data(posts: dict) -> List[dict]:
    print("in func3")

    post_list = []
    if 'data' in posts and 'children' in posts['data']:
        for post in posts['data']['children']:
            sentiment = sentiments_model.sentiment_classify(post['data']['title'])
            post_list.append(
                {
                    'subreddit': post['data']['subreddit'],
                    'title': post['data']['title'],
                    'sentiment' : sentiment,
                    'selftext': post['data']['selftext'],
                    'upvote_ratio': post['data']['upvote_ratio'],
                    'ups': post['data']['ups'],
                    'downs': post['data']['downs'],
                    'score': post['data']['score']
                })
    else:
        print("Unexpected response structure:", posts)

    return post_list
    

def get_posts_from_reddit(subreddit: str, category: str):
    print("get_posts_from_reddit")
    posts = get_posts_by_subreddit_and_category(subreddit, category)
    # print(posts)
    return get_format_posts_data(posts)


def create_reddit_search(db: Session, reddit: str, category: reddit_schema.ModelRedditCategory, user_id: int):
    # Create an instance of RedditSearch model
    db_reddit_search = reddit_model.RedditSearch(user_id=user_id, reddit=reddit, category=category)
    
    # Add the instance to the session
    db.add(db_reddit_search)
    
    # Commit the transaction to the database
    db.commit()
    
    # Refresh the instance to get the updated values
    db.refresh(db_reddit_search)
    
    return db_reddit_search


def create_subreddits_search(db: Session, subreddits: list[subreddit_schema.SubredditSearchCreate]):

    # Create an instance of RedditSearch model

    db_subreddits_search = []
    for subreddit in subreddits:
        db_subreddit_search = subreddit_model.SubredditSearch(reddit_id=subreddit.reddit_id, title=subreddit.title, selftext=subreddit.selftext, sentiment=subreddit.sentiment, ups=subreddit.ups, downs=subreddit.downs, score=subreddit.score)
    
        # Add the instance to the session
        db.add(db_subreddit_search)
    
        # Commit the transaction to the database
        db.commit()
    
        # Refresh the instance to get the updated values
        db.refresh(db_subreddit_search)
        db_subreddits_search.append(db_subreddit_search)
    
    return db_subreddits_search


def get_recent_searches_for_user(db: Session, user_id: int):
    return db.query(reddit_model.RedditSearch).filter(reddit_model.RedditSearch.user_id == user_id).all()


def get_history_posts_by_reddit_id(db: Session, reddit_id: int):
    return db.query(subreddit_model.SubredditSearch).filter(subreddit_model.SubredditSearch.reddit_id == reddit_id).all()