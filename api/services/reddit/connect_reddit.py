import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


CLIENT_ID : str = os.getenv('REDDIT_CLIENT_ID')
SECRET_KEY : str = os.getenv('REDDIT_SECRET_KEY')
USERNAME : str = os.getenv('REDDIT_USERNAME')
PASSWORD : str = os.getenv('REDDIT_PASSWORD')

import requests

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
    'grant_type': 'password',
    'username': USERNAME,
    'password': PASSWORD
}

headers = {'User-Agent': 'MyApi/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth = auth, data = data, headers = headers, params={'limit': '100', 'after': 't3_1ae05y3'})

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}

# post['data'].keys()

# print(df)

# print(post['kind'])
# print(post['data']['id'])

# post['kind'] + '_' + post['data']['id'] => uniq id

def get_posts_by_subreddit(subreddit:str):
    #for default get the new posts, default amount = 25
    return get_posts_by_subreddit_and_category(subreddit=subreddit, category="new")


def get_posts_by_subreddit_and_category(subreddit:str, category:str):
    res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/{category}', headers = headers)
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



# print(get_posts_by_subreddit("python"))