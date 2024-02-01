import os
from dotenv import load_dotenv
from pathlib import Path
import requests

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


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
    # for default get the new posts, default amount = 25
    return get_posts_by_subreddit_and_category(subreddit=subreddit, category="new")


def get_posts_by_subreddit_and_category(subreddit: str, category: str):
    headers = get_headers_from_connection_to_reddit_by_access_token()
    res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/{category}', headers=headers)
    
    post_list = []
    for post in res.json()['data']['children']:
        post_list.append(
            {
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['upvote_ratio'],
                'ups': post['data']['ups'],
                'downs': post['data']['downs'],
                'score': post['data']['score']
            })

    return post_list
