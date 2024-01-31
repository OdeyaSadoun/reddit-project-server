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

# requests.get('https://oauth.reddit.com/api/v1/me', headers = headers).json()

res = requests.get('https://oauth.reddit.com/r/python/hot', headers = headers) 

import pandas as pd

df = pd.DataFrame()

for post in res.json()['data']['children']:
    df = df.append({
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'upvote_ratio': post['data']['upvote_ratio'],
        'ups': post['data']['ups'],
        'downs': post['data']['downs'],
        'score': post['data']['score']
    }, ignore_index=True)

post['data'].keys()

print(df)

print(post['kind'])
print(post['data']['id'])

# post['kind'] + '_' + post['data']['id'] => uniq id




 