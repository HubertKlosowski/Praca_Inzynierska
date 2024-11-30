import os
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from model.api_keys import public_key, secret_key
import praw
from datetime import datetime
from praw.models import MoreComments
from langdetect import detect, DetectorFactory

import spacy
from deep_translator import GoogleTranslator  # tłumaczenie znaczenia emotek
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


def limit_lang(df: pd.DataFrame, lang: str = 'en') -> pd.DataFrame:  # pozostawienie tylko wpisow w danym jezyku
    df['text'] = df['text'].apply(lambda x: x.strip())
    if 'lang' not in df.columns:
        df['lang'] = df['text'].apply(lambda x: detect(x))
    df.drop(index=df.loc[(df['lang'] != lang), :].index, inplace=True)
    df.drop(columns=['lang'], inplace=True)
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

    merged.drop_duplicates(subset=['text'], keep='first', inplace=True)  # usuniecie duplikatow
    merged.dropna(inplace=True)  # usuniecie wartosci NaN
    merged['len'] = merged['text'].apply(lambda x: len(x.split()))
    merged.drop(merged.loc[
                    (merged['len'] < merged['len'].quantile(0.05)) |
                    (merged['len'] >= merged['len'].quantile(0.95))].index, inplace=True)

    merged = limit_lang(merged, lang=lang)  # pozostawienie tylko wpisow w danym jezyku

    if for_train:
        merged['label'] = merged['label'].astype(int)
        counts = merged['label'].value_counts()

        if counts[0] > counts[1]:
            sample = counts[0] - counts[1]
            merged.drop(index=merged.loc[merged['label'] == 0].sample(n=sample).index, inplace=True)
        else:
            sample = counts[1] - counts[0]
            merged.drop(merged.loc[merged['label'] == 1].sample(n=sample).index, inplace=True)

        merged = merged.sample(frac=1)  # shuffle

    merged.drop(columns=['len'], inplace=True)
    merged.reset_index(drop=True, inplace=True)

    merged.dropna(subset=['text'], inplace=True)

    return merged


# Funkcja odpowiedzialna jest za przygotowanie zbiorów:
# usunięcie adresów URL
# zmiana emotek na ich znaczenie (tylko dla języka angielskiego)
# usunięcie nadmiarowych spacji
# usuniecie znaków interpunkcyjnych
# usuniecie stop-words
# stemming
def preprocess_dataset(dataset: pd.DataFrame, lang: str = 'pl') -> pd.DataFrame:
    lang_resource = spacy.load('en_core_web_sm') if lang == 'en' else spacy.load('pl_core_news_sm')
    lang_resource.add_pipe('emoji', first=True)

    stemmer = PorterStemmer() if lang == 'en' else Stemmer.polimorf()

    url_pattern = r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
    dataset['text'] = dataset['text'].apply(lambda sentence: re.sub(url_pattern, '', sentence))
    dataset['text'] = dataset['text'].apply(lambda sentence: sentence.strip())

    dataset['text'] = dataset['text'].apply(lambda sentence: lang_resource(sentence))
    dataset['text'] = dataset['text'].apply(
        lambda tokens: [token for token in tokens if not token.is_punct]
    )
    dataset['text'] = dataset['text'].apply(
        lambda tokens: [token for token in tokens if not token.is_stop]
    )

    if lang == 'pl':
        translator = GoogleTranslator(source='auto', target='pl')  # do tłumaczenia znaczenia emotek
        dataset['text'] = dataset['text'].apply(
            lambda tokens: [translator.translate(token._.emoji_desc) if token._.is_emoji else token.text for token in tokens]
        )
        dataset['text'] = dataset['text'].apply(lambda tokens: [stemmer(token) for token in tokens])
    else:
        dataset['text'] = dataset['text'].apply(
            lambda tokens: [token._.emoji_desc if token._.is_emoji else token.text for token in tokens]
        )
        dataset['text'] = dataset['text'].apply(lambda tokens: [stemmer.stem(token) for token in tokens])

    dataset['text'] = dataset['text'].apply(
        lambda tokens: ' '.join([str(token) for token in tokens if token is not None])
    )

    return dataset

# obsluga zbyt dlugich wpisow
def drop_too_long(df: pd.DataFrame, tokenizer) -> pd.DataFrame:
    df_copy = df.copy(deep=True)
    limit = 256
    df_copy['len'] = df_copy['text'].apply(lambda sentence: len(tokenizer.tokenize(sentence)))
    df_copy.drop(df_copy.loc[df_copy['len'] > limit, ['text']].index, inplace=True)  # wpisy zbyt dlugie
    df_copy.drop(columns=['len'], inplace=True)

    return df_copy


def read_json_tweet(file_name):
    with open(os.path.join('data', 'tweets', file_name), 'r') as file:
        data = json.load(file)
    return {'text': data['text'], 'lang': data['lang']}


def prepare_tweets():
    posts = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        res = [executor.submit(read_json_tweet, f) for f in os.listdir(os.path.join('data', 'tweets'))]
        for f in as_completed(res):
            posts.append(f.result())

    tweets = pd.DataFrame(posts)
    tweets = limit_lang(tweets)
    tweets = preprocess_dataset(tweets, lang='en')

    return tweets


# Przetworzone wpisy w obu językach (zbiór treningowy/walidacyjny)
# train_preprocessed_english_dataset = preprocess_dataset(merge_datasets(lang='en', for_train=True), lang='en')
# train_preprocessed_english_dataset.to_csv(os.path.join('data', 'final', 'train_preprocessed_english_dataset.csv'), index=False)
#
# train_preprocessed_polish_dataset = preprocess_dataset(merge_datasets(lang='pl', for_train=False), lang='pl')  # brak wskazanych klas
# train_preprocessed_polish_dataset.to_csv(os.path.join('data', 'final', 'train_preprocessed_polish_dataset.csv'), index=False)

# Przetworzone wpisy w obu językach (zbiór testowy)
# test_preprocessed_english_dataset = prepare_tweets()
# test_preprocessed_english_dataset.to_csv(os.path.join('data', 'final', 'test_preprocessed_english_dataset.csv'), index=False)
