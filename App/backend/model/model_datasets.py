import json
import os
import re
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from langdetect import DetectorFactory, detect

DetectorFactory.seed = 0

import numpy as np
import praw
import requests
import spacy
import torch
from datasets import Dataset, DatasetDict
from deep_translator import GoogleTranslator  # tłumaczenie znaczenia emotek
from googletrans import Translator
from nltk.stem import PorterStemmer  # stemming dla języka angielskiego
from praw.models import MoreComments
from pystempel import Stemmer  # stemming dla języka polskiego
from sklearn.model_selection import train_test_split

from model.api_keys import public_key, secret_key, microsoft_api_key, save_model_token

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from transformers import (AutoModelForSequenceClassification, TextClassificationPipeline,
                          TrainingArguments, Trainer, DataCollatorWithPadding, AutoTokenizer)
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from huggingface_hub import login, logout


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
# lista wszystkich polskich subredditów: https://www.reddit.com/r/Polska/wiki/subreddity/
#
# similar_topics = ['stan depresyjny', 'stan depresji', 'alkoholizm', 'stany lękowe', 'samotność', 'samookaleczanie',
#                   'samobójstwo', 'żałoba', 'depresja']
# final = pd.DataFrame()
# for topic in similar_topics:
#     dataframe = save_dataframe_reddit(topic)
#     final = pd.concat([final, dataframe])
# final.drop_duplicates(subset=['title', 'text'], keep='first', inplace=True)
# final.to_csv(os.path.join('data', 'polish_reddit_posts_1.csv'), index=False)


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


def detect_lang(df: pd.DataFrame) -> str:
    translator = Translator()
    df['text'] = df['text'].apply(lambda x: x.strip())
    df['lang'] = df['text'].apply(lambda x: translator.detect(x).lang)
    langs = df['lang'].value_counts()
    df.drop(columns=['lang'], inplace=True)
    return langs.idxmax(axis=0)


def extract_comments() -> pd.DataFrame:
    comments = pd.read_csv(os.path.join('data', 'pl', 'polish_reddit_posts.csv'))['comments'].to_frame()
    comments['comments'] = comments['comments'].apply(lambda x: eval(x))  # konwersja listy w stringu do prawdziwej listy
    comments = comments.explode('comments')
    comments.rename(columns={'comments': 'text'}, inplace=True)
    comments.reset_index(drop=True, inplace=True)
    comments.to_csv(os.path.join('data', 'pl', 'polish_reddit_comments.csv'), index=False)
    return comments


def create_dataset(dataframe: pd.DataFrame, split_train_test: bool) -> DatasetDict:
    dt = DatasetDict()
    if split_train_test:
        dataframe['label'] = dataframe['label'].astype(int)
        x_train, x_test = train_test_split(dataframe, test_size=0.3, random_state=4)
        training = pd.DataFrame(x_train, columns=dataframe.columns).reset_index(drop=True)
        testing = pd.DataFrame(x_test, columns=dataframe.columns).reset_index(drop=True)
        dt['train'] = Dataset.from_pandas(training)
        dt['test'] = Dataset.from_pandas(testing)

    else:
        dt['test'] = Dataset.from_pandas(dataframe)
    return dt


# Połączenie zbiorów w jeden + ujednolicenie nazewnictwa kolumn
def merge_datasets(lang: str = 'en', for_train: bool = False) -> pd.DataFrame:
    merged = pd.DataFrame()
    columns = ['text', 'label'] if for_train and lang == 'en' else ['text']

    for d in os.listdir(os.path.join('data', lang)):
        dataframe = pd.read_csv(os.path.join('data', lang, d))

        if lang == 'pl' and d == 'polish_reddit_posts.csv':
            dataframe = dataframe[columns]

        dataframe.dropna(inplace=True)

        for i, source_col in enumerate(dataframe.columns):  # ujednolicenie nazewnictwa
            dataframe.rename(columns={source_col: columns[i]}, inplace=True)

        dataframe = dataframe[columns].reset_index(drop=True)

        merged = pd.concat([merged, dataframe], axis=0)

    merged.drop_duplicates(subset=['text'], keep='first', inplace=True)  # usuniecie duplikatow
    merged.dropna(inplace=True)  # usuniecie wartosci NaN
    merged['len'] = merged['text'].apply(lambda x: len(x.split()))

    merged.drop(merged.loc[
                    (merged['len'] <= merged['len'].quantile(0.05)) |
                    (merged['len'] >= merged['len'].quantile(0.95))].index, inplace=True
                )

    if for_train:
        merged = balance_dataset(merged)

    merged.drop(columns=['len'], inplace=True)
    merged.reset_index(drop=True, inplace=True)

    return merged


def balance_dataset(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['label'] = dataframe['label'].astype(int)
    counts = dataframe['label'].value_counts()

    if counts[0] > counts[1]:
        sample = counts[0] - counts[1]
        dataframe.drop(index=dataframe.loc[dataframe['label'] == 0].sample(n=sample).index, inplace=True)
    else:
        sample = counts[1] - counts[0]
        dataframe.drop(index=dataframe.loc[dataframe['label'] == 1].sample(n=sample).index, inplace=True)

    return dataframe.sample(frac=1).reset_index(drop=True)


# Funkcja odpowiedzialna jest za przygotowanie zbiorów:
# usunięcie adresów URL
# zmiana emotek na ich znaczenie (tylko dla języka angielskiego)
# usunięcie nadmiarowych spacji
# usuniecie znaków interpunkcyjnych
# usuniecie stop-words
# stemming
def preprocess_dataset(dataframe: pd.DataFrame, lang: str = 'en') -> pd.DataFrame:
    lang_resource = spacy.load('en_core_web_sm') if lang == 'en' else spacy.load('pl_core_news_sm')
    lang_resource.add_pipe('emoji', first=True)

    stemmer = PorterStemmer() if lang == 'en' else Stemmer.polimorf()

    url_pattern = r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
    dataframe['text'] = dataframe['text'].apply(lambda sentence: re.sub(url_pattern, '', sentence))
    dataframe['text'] = dataframe['text'].apply(lambda sentence: sentence.strip())
    dataframe['text'] = dataframe['text'].apply(lambda sentence: lang_resource(sentence))
    dataframe['text'] = dataframe['text'].apply(
        lambda tokens: [token for token in tokens if not token.is_punct]
    )
    dataframe['text'] = dataframe['text'].apply(
        lambda tokens: [token for token in tokens if not token.is_stop]
    )
    if lang == 'pl':
        translator = GoogleTranslator(source='auto', target='pl')  # do tłumaczenia znaczenia emotek
        dataframe['text'] = dataframe['text'].apply(
            lambda tokens: [translator.translate(token._.emoji_desc) if token._.is_emoji else token.text for token in tokens]
        )
        dataframe['text'] = dataframe['text'].apply(lambda tokens: [stemmer(token) for token in tokens])
    else:
        dataframe['text'] = dataframe['text'].apply(
            lambda tokens: [token._.emoji_desc if token._.is_emoji else token.text for token in tokens]
        )
        dataframe['text'] = dataframe['text'].apply(lambda tokens: [stemmer.stem(token) for token in tokens])
    dataframe['text'] = dataframe['text'].apply(
        lambda tokens: ' '.join([str(token) for token in tokens if token is not None])
    )

    return dataframe

# obsluga zbyt dlugich wpisow
def drop_too_long(df: pd.DataFrame, tokenizer) -> pd.DataFrame:
    df_copy = df.copy(deep=True)
    limit = 512
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


# Funkcja do realizacji tłumaczenia polskich wpisów na angielskie
def translate_part(body, constructed_url, headers):
    request = requests.post(constructed_url, json=body, headers=headers)
    response = request.json()
    return response


# Funkcja do realizacji:
# 1) połączenia z API do Azure AI Services i Translatora (płatne więc uważać trzeba)
# 2) podziału zbioru na części z powodu ograniczeń dla request
# 3) połączenia przetłumaczonych części w jeden zbiór
# 4) zapis do pliku
def translate_to_en(dataframe: pd.DataFrame):
    endpoint = 'https://api.cognitive.microsofttranslator.com'
    location = 'germanywestcentral'
    path = '/translate?api-version=3.0&from=pl&to=en'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': microsoft_api_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    text_polish = dataframe['text'].values.tolist()

    # podział na części
    # API nie jest w stanie przyjąć całego zbioru naraz
    # i tylko przyjmuje dane w określonym formacie
    parts = 300
    num_in_part = (len(text_polish) // parts) + 1
    text_polish = [text_polish[i * num_in_part : (i + 1) * num_in_part] for i in range(parts)]
    text_polish = [[{'text': row} for row in part] for part in text_polish]
    text_polish = [part for part in text_polish if len(part) != 0]

    # wykonanie tłumaczenia z polskiego na angielski
    polish_translated = []
    for part in text_polish:
        polish_translated.append(translate_part(part, constructed_url, headers))
        time.sleep(2)  # konieczne aby API nie zwracało error

    # połączenie danych w jeden DataFrame
    translated = pd.DataFrame()
    for translated_part in polish_translated:
        tmp1 = pd.DataFrame(translated_part)
        tmp1['translations'] = tmp1['translations'].apply(lambda x: x[0]['text'])
        tmp1.rename(columns={'translations': 'text'}, inplace=True)
        translated = pd.concat([translated, tmp1], axis=0)

    # Zapis przetłumaczonych wpisów
    translated.reset_index(drop=True, inplace=True)
    translated.to_csv('data/final/polish_translated.csv', index=False)

    return translated


# Predykcje modeli odpowiedzialnych za analizę
# sentymentu, emocji w zbiorze polskim i depresji tego zbioru w języku angielskim
def return_pred(model_path: str, dataframe: pd.DataFrame, result_column: str) -> pd.DataFrame:
    res = predict(model_path, dataframe, True)
    res = pd.DataFrame(np.argmax(res.to_numpy(), axis=1), columns=[result_column])
    return res


# Funkcja łączy rezultaty z modeli:
# 1) analiza sentymentu w wpisach po polsku:
#       negatywny, pozytywny, neutralny, dwuznaczny
# 2) wykrycie emocji w wpisach po polsku:
#       złość, strach, obrzydzenie, smutek, szczęście, żadna z wymienionych
# 3) wykrycie depresji w wpisach przetłumaczonych na język angielski:
#       posiada/nie posiada depresji (LABEL_1, LABEL_0)
# Ostatecznie podjęty jest wybór, które podgrupy posiadają depresję na podstawie obliczonych składowych
def tag_polish(dataframe: pd.DataFrame) -> pd.DataFrame:
    # rezultaty GPT2 dla sentymentu
    sentiment = return_pred('nie3e/sentiment-polish-gpt2-large', dataframe, 'sentiment')

    # rezultaty RoBERTa dla emocji
    emotion = return_pred('visegradmedia-emotion/Emotion_RoBERTa_polish6', dataframe, 'emotion')

    # rezultaty mojego BERT dla depresji w języku angielskim
    # english = pd.read_csv('data/final/polish_translated.csv')
    # en_depress = return_pred('depression-detect/bert-base', english, 'en_depress')

    # złączenie cząstkowych rezultatów
    polish_results = pd.concat([dataframe, sentiment, emotion], axis=1)

    # wskazanie, które podgrupy danych uznaję za posiadające depresję
    # Grupy:
    # 1) ma negatywny sentyment, posiada depresję w języku angielskim i emocje lęku, smutku lub obrzydzenia
    # 2) ma dwuznaczny sentyment, posiada depresję w języku angielskim i emocje lęku lub smutku
    # 3) ma neutralny sentyment, posiada depresję w języku angielskim i emocje lęku lub smutku
    polish_results.loc[(polish_results['sentiment'] == 3) & ((polish_results['emotion'] == 2) |
                                                             (polish_results['emotion'] == 4) |
                                                             (polish_results['emotion'] == 5)), 'label'] = 1
    polish_results.loc[(polish_results['sentiment'] == 0) & ((polish_results['emotion'] == 2) |
                                                             (polish_results['emotion'] == 4)), 'label'] = 1
    polish_results.loc[(polish_results['sentiment'] == 1) & ((polish_results['emotion'] == 2) |
                                                             (polish_results['emotion'] == 4)), 'label'] = 1

    polish_results.fillna(0, inplace=True)
    polish_results['label'] = polish_results['label'].astype(int)

    polish_results.drop(columns=['emotion', 'sentiment'], inplace=True)  # usunięcie niepotrzebnych danych
    polish_results.reset_index(drop=True, inplace=True)

    return polish_results


def apply_tokenizer(tokenizer, row):
    return tokenizer(row['text'], truncation=True)


def compute_metrics(logits):
    y_pred, y_true = logits
    y_pred = np.argmax(y_pred, axis=1)
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred),
    }


def fine_tune(model_path: str):
    login(token=save_model_token)

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    dataset = create_dataset(
        pd.read_csv(os.path.join('data', 'final', 'train_preprocessed_english.csv'))
        if model_path == 'bert-base' or model_path == 'bert-large'
        else pd.read_csv(os.path.join('data', 'final', 'train_preprocessed_polish.csv')).dropna(),
        split_train_test=True
    )

    tokenized_dataset = dataset.map(lambda x: apply_tokenizer(tokenizer, x), batched=True)
    id2label = { 0: 'non-depressed', 1: 'depressed' }
    label2id = { 'non-depressed': 0, 'depressed': 1 }

    model = AutoModelForSequenceClassification.from_pretrained(
        model_path,
        num_labels=2,
        id2label=id2label,
        label2id=label2id
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    training_args = TrainingArguments(
        output_dir=f'{model_path}-depression',
        learning_rate=2e-5,
        per_device_train_batch_size=32,
        per_device_eval_batch_size=64,
        num_train_epochs=10,
        weight_decay=0.01,
        eval_strategy='epoch',
        save_strategy='epoch',
        load_best_model_at_end=True,
        log_level='error',
        push_to_hub=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset['train'],
        eval_dataset=tokenized_dataset['test'],
        processing_class=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics
    )

    trainer.train()

    trainer.push_to_hub()

    logout()


def predict(model_path: str, dataframe: pd.DataFrame, for_train: bool = True, login_token: str = None) -> pd.DataFrame:
    if login_token is not None:
        login(token=save_model_token)

    dataset = create_dataset(dataframe, split_train_test=False)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    pipe = TextClassificationPipeline(
        model=model,
        tokenizer=tokenizer,
        top_k=None,
        device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    )

    if for_train:
        predictions = prepare_predictions(
            pipe(dataset['test']['text'], **{'truncation': True, 'max_length': 512}),
            dataframe.index
        )
    else:
        try:
            predictions = prepare_predictions(
                pipe(dataset['test']['text']),
                dataframe.index
            )
        except RuntimeError:
            under_limit = drop_too_long(dataframe, tokenizer)
            dataset_under_limit = create_dataset(
                under_limit, split_train_test=False
            )
            predictions_under_limit = prepare_predictions(
                pipe(dataset_under_limit['test']['text']),
                under_limit.index
            )
            predictions = pd.concat([under_limit, predictions_under_limit], axis=1)
            predictions = pd.merge(dataframe, predictions, how='left', on='text')
            predictions.drop(columns=['text'], inplace=True)
            predictions.fillna(-1, inplace=True)

    if login_token is not None:
        logout()

    return predictions


def prepare_predictions(pred, df_index) -> pd.DataFrame:
    return pd.DataFrame([{pair['label']: pair['score'] for pair in row} for row in pred], index=df_index)


# fine_tune('depression-detect/bert-base')
# fine_tune('depression-detect/bert-large')
# fine_tune('roberta-base')
# fine_tune('roberta-large')

# Przetworzone wpisy dla języka angielskiego (zbiór treningowy)
# if 'train_english.csv' in os.listdir(os.path.join('data', 'final')):
#     train_english = pd.read_csv(os.path.join('data', 'final', 'train_english.csv'))
# else:
#     train_english = merge_datasets(lang='en', for_train=True)
#     train_english.to_csv(os.path.join('data', 'final', 'train_english.csv'), index=False)
#
# train_preprocessed_english = preprocess_dataset(train_english, lang='en').dropna()
# train_preprocessed_english.to_csv(os.path.join('data', 'final', 'train_preprocessed_english.csv'), index=False)

# Wygenerowanie otagowanego zbioru polskiego
# if 'train_polish.csv' in os.listdir(os.path.join('data', 'final')):
#     train_polish = pd.read_csv(os.path.join('data', 'final', 'train_polish.csv'))
# else:
#     train_polish = tag_polish(merge_datasets(lang='pl', for_train=False))
#     train_polish.to_csv(os.path.join('data', 'final', 'train_polish.csv'), index=False)
#
# train_preprocessed_polish = balance_dataset(preprocess_dataset(train_polish, lang='pl')).dropna()
# train_preprocessed_polish.to_csv(os.path.join('data', 'final', 'train_preprocessed_polish.csv'), index=False)

# Przetworzone wpisy w języku angielskim (zbiór testowy)
# test_preprocessed_english_dataset = prepare_tweets()
# test_preprocessed_english_dataset.to_csv(os.path.join('data', 'final', 'test_preprocessed_english.csv'), index=False)