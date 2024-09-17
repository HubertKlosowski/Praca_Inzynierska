import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from api_keys import public_key, secret_key
import praw
from datetime import datetime
from praw.models import MoreComments


# Dla zbioru danych MDDL z githuba
def get_path_to_mddl() -> str:
    path = os.getcwd()
    while 'Dataset' not in os.listdir(path):
        path = os.path.join(path, '..')
        if path == os.path.abspath(os.path.join(path, '..')):
            raise FileNotFoundError("Nie znaleziono katalogu 'Dataset' w żadnym z nadrzędnych katalogów.")
    return os.path.join(path, 'Dataset')


def get_dataframe_twitter(path: str) -> pd.DataFrame:
    tweets = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        res = [executor.submit(read_json_tweet, os.path.join(path, f), 0) for f in os.listdir(path)]
        for f in as_completed(res):
            tweets.append(f.result())
    df = pd.DataFrame(tweets)
    return df


def read_json_tweet(filename: str, label: int) -> dict:
    file = open(filename)
    data = json.load(file)
    file.close()
    return {
        'user_id': data['user']['id_str'],
        'tweet_id': data['id_str'],
        'in_reply_to_status_id': data['in_reply_to_status_id'],
        'in_reply_to_user_id': data['in_reply_to_user_id'],
        'created_at': data['created_at'],
        'text': data['text'],
        'retweet_count': data['retweet_count'],
        'favorite_count': data['favorite_count'],
        'favorited': data['favorited'],
        'retweeted': data['retweeted'],
        'lang': data['lang'],
        'depresed': label,
    }


# Dla wpisów z języka polskiego z Reddita
def save_dataframe_reddit(search_by: str) -> pd.DataFrame:
    reddit = praw.Reddit(
        client_id=public_key,
        client_secret=secret_key,
        user_agent='Polish Depression',
    )

    posts = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        res = [executor.submit(read_reddit_post, s) for s in reddit.subreddit('Polska').search(search_by, limit=None)]
        for f in as_completed(res):
            posts.append(f.result())

    return pd.DataFrame(posts)


def read_reddit_post(sub: praw.reddit.Submission) -> dict:
    return {
        'created_utc': datetime.fromtimestamp(sub.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        'title': sub.title,
        'text': sub.selftext,
        'score': sub.score,
        'upvote_ratio': sub.upvote_ratio,
        'num_comments': sub.num_comments,
        'over_18': sub.over_18,
        'comments': [c.body for c in sub.comments if not isinstance(c, MoreComments)],
    }


# Przykłady użycia:
# dataframe1 = get_dataframe_twitter(os.path.join(get_path_to_mddl(), 'unlabeled', 'tweet'))
# dataframe2 = get_dataframe_twitter(os.path.join(path_to_dataset, 'unlabeled', 'positive', 'tweet'))

# lista wszystkich polskich subredditów: https://www.reddit.com/r/Polska/wiki/subreddity/

# similar_topics = ['stan depresyjny', 'stan depresji', 'alkoholizm', 'stany lękowe', 'samotność', 'samookaleczanie',
#                   'samobójstwo', 'żałoba', 'depresja']
# final = pd.DataFrame()
# for topic in similar_topics:
#     df = save_dataframe_reddit(topic)
#     final = pd.concat([final, df])
# final.drop_duplicates(subset=['title', 'text'], keep='first', inplace=True)
# final.to_csv(os.path.join('..', 'data', 'polish_reddit_posts.csv'), index=False)
