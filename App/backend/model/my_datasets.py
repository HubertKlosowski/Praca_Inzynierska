import os

import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from model.api_keys import public_key, secret_key
import praw
from datetime import datetime
from praw.models import MoreComments
from langdetect import detect, DetectorFactory
from transformers import AutoTokenizer

import nltk
import string
import emoji  # do wykrycia emotek
import re
from nltk.stem import PorterStemmer  # stemming dla języka angielskiego
from pystempel import Stemmer  # stemming dla języka polskiego

DetectorFactory.seed = 0


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
# Przykład użycia
"""
    lista wszystkich polskich subredditów: https://www.reddit.com/r/Polska/wiki/subreddity/

    similar_topics = ['stan depresyjny', 'stan depresji', 'alkoholizm', 'stany lękowe', 'samotność', 'samookaleczanie',
                      'samobójstwo', 'żałoba', 'depresja']
    final = pd.DataFrame()
    for topic in similar_topics:
        dataframe = save_dataframe_reddit(topic)
        final = pd.concat([final, dataframe])
    final.drop_duplicates(subset=['title', 'text'], keep='first', inplace=True)
    final.to_csv(os.path.join('data', 'polish_reddit_posts_1.csv'), index=False)
"""


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


def limit_lang(df: pd.DataFrame, lang: str = 'en') -> pd.DataFrame:  # usunięcie wpisów nie w wybranym języku
    if 'lang' not in df.columns:
        df['lang'] = df['text'].apply(lambda x: detect(x))
    df.drop(index=df.loc[(df['lang'] != lang), :].index, inplace=True)
    df.drop(columns=['lang'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def limit_length(df: pd.DataFrame, limit_to: int) -> pd.DataFrame:  # usunięcie wpisów zbyt długich
    df['len'] = df['text'].apply(lambda x: len(x.split()))
    df.drop(index=df.loc[df['len'] > limit_to, :].index, inplace=True)
    df.drop(columns=['len'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def extract_comments() -> pd.DataFrame:
    comments = pd.read_csv(os.path.join('data', 'pl', 'polish_reddit_posts.csv'))['comments'].to_frame()
    comments['comments'] = comments['comments'].apply(lambda x: eval(x))  # konwersja listy w stringu do prawdziwej listy
    comments = comments.explode('comments')
    comments.rename(columns={'comments': 'text'}, inplace=True)
    comments.reset_index(drop=True, inplace=True)
    comments.to_csv(os.path.join('data', 'pl', 'polish_reddit_comments.csv'), index=False)
    return comments


# Połączenie wielu zbiorów w jeden + ujednolicenie nazewnictwa kolumn
def merge_datasets(lang = 'pl', for_train = False) -> pd.DataFrame:
    merged = pd.DataFrame()
    columns = ['text', 'label'] if for_train and lang == 'en' else ['text']

    for d in os.listdir(os.path.join('data', lang)):
        dataset = pd.read_csv(os.path.join('data', lang, d))

        if lang == 'pl' and d == 'polish_reddit_posts.csv':
            dataset['text'] = dataset['title'] + ' ' + dataset['text']
            dataset = dataset[columns]

        dataset.dropna(inplace=True)

        for i, source_col in enumerate(dataset.columns):  # ujednolicenie nazewnictwa
            dataset.rename(columns={source_col: columns[i]}, inplace=True)

        dataset = dataset[columns].reset_index(drop=True)

        merged = pd.concat([merged, dataset], axis=0)

    return merged


# Funkcja odpowiedzialna jest za przygotowanie zbiorów:
# usunięcie adresów URL
# zmiana emotek na ich znaczenie (tylko dla języka angielskiego)
# usunięcie nadmiarowych spacji
# usuniecie znaków interpunkcyjnych
# usuniecie stop-words
# stemming
def preprocess_dataset(dataset: pd.DataFrame, lang = 'pl') -> pd.DataFrame:
    stemmer = PorterStemmer() if lang == 'en' else Stemmer.polimorf()

    url_pattern = r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'  # GOTOWIEC Z INTERNETU
    dataset['text'] = dataset['text'].apply(lambda sentence: re.sub(url_pattern, '', sentence))

    if lang == 'en':
        dataset['text'] = dataset['text'].apply(lambda sentence: emoji.demojize(sentence))

    dataset['text'] = dataset['text'].apply(lambda sentence: sentence.strip())
    dataset['text'] = dataset['text'].apply(lambda sentence: nltk.word_tokenize(sentence))
    dataset['text'] = dataset['text'].apply(
        lambda tokens: [token for token in tokens if token not in string.punctuation])
    dataset['text'] = dataset['text'].apply(
        lambda tokens: [token for token in tokens if token.lower() not in nltk.corpus.stopwords.words('polish' if lang == 'pl' else 'english')])

    if lang == 'pl':
        dataset['text'] = dataset['text'].apply(lambda tokens: [stemmer(token) for token in tokens])
    else:
        dataset['text'] = dataset['text'].apply(lambda tokens: [stemmer.stem(token) for token in tokens])

    dataset['text'] = dataset['text'].apply(
        lambda tokens: ' '.join([str(token) for token in tokens if token is not None])
    )

    dataset.dropna(inplace=True)

    return dataset


# funkcja sluzaca do podzialu zbyt dlugich sekwencji tokenow na mniejsze czesci o dlugosci limitu tokenizatora
def slice_too_long(tokens, limit) -> list:
    return [tokens[limit * i:limit * (i + 1)] for i in range(len(tokens) // limit + 1)]


# obsluga zbyt dlugich wpisow
def manage_too_long(df: pd.DataFrame, tokenizer) -> tuple[pd.DataFrame, pd.DataFrame]:
    limit = 256

    df['text'] = df['text'].apply(lambda x: tokenizer.tokenize(x))  # tokenizacja zdań
    df['len'] = df['text'].apply(lambda x: len(x))
    over_limit = df.loc[df['len'] > limit, ['text']].reset_index(drop=True)  # wpisy zbyt dlugie
    under_limit = df.loc[df['len'] <= limit, ['text']].reset_index(drop=True)

    over_limit['text'] = over_limit['text'].apply(lambda row: slice_too_long(row, limit))  # podzial wpisow na krotsze czesci
    over_limit = over_limit.explode(column='text')  # rozbicie df po kolumnie 'text'
    over_limit['text'] = over_limit['text'].apply(lambda row: tokenizer.convert_tokens_to_string(row))  # konwersja tokenow na string
    under_limit['text'] = under_limit['text'].apply(lambda row: tokenizer.convert_tokens_to_string(row))

    return over_limit, under_limit
# Przykład użycia
"""
    long = manage_too_long(
        pd.read_csv('data/test_too_long.csv'),
        AutoTokenizer.from_pretrained('bert-base-uncased')
    )

    print(long)
"""



# Przetworzone wpisy w obu językach
# preprocess_dataset(merge_datasets(lang='en', for_train=True), lang='en').to_csv(os.path.join('data', 'final', 'preprocessed_english_dataset.csv'), index=False)
# preprocess_dataset(merge_datasets(lang='pl', for_train=False), lang='pl').to_csv(os.path.join('data', 'final', 'preprocessed_polish_dataset.csv'), index=False)
# extract_comments()

# Nie przetworzone wpisy w języku polskim
# merge_datasets(lang='pl', for_train=True).to_csv(os.path.join('data', 'final', 'polish_dataset.csv'), index=False)