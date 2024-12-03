import json
import os
import re
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

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

from model.api_keys import public_key, secret_key, microsoft_api_key

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from transformers import (AutoModelForSequenceClassification, TextClassificationPipeline,
                          TrainingArguments, Trainer, DataCollatorWithPadding, AutoTokenizer)
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from model.api_keys import save_model_token
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
    translator = Translator()
    df['text'] = df['text'].apply(lambda x: x.strip())
    if 'lang' not in df.columns:
        df['lang'] = df['text'].apply(lambda x: translator.detect(x).lang)
    df.drop(index=df.loc[(df['lang'] != lang), :].index, inplace=True)
    df.drop(columns=['lang'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def detect_lang(df: pd.DataFrame) -> str:
    translator = Translator()
    df['text'] = df['text'].apply(lambda x: x.strip())
    df['lang'] = df['text'].apply(lambda x: translator.detect(x).lang)
    langs = df['lang'].value_counts()
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


# Połączenie wielu zbiorów w jeden + ujednolicenie nazewnictwa kolumn
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
        merged['label'] = merged['label'].astype(int)
        counts = merged['label'].value_counts()

        if counts[0] > counts[1]:
            sample = counts[0] - counts[1]
            merged.drop(index=merged.loc[merged['label'] == 0].sample(n=sample).index, inplace=True)
        else:
            sample = counts[1] - counts[0]
            merged.drop(index=merged.loc[merged['label'] == 1].sample(n=sample).index, inplace=True)

        merged = merged.sample(frac=1)  # shuffle

    merged.drop(columns=['len'], inplace=True)
    merged.reset_index(drop=True, inplace=True)

    return merged


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


# Predykcje modelu Roberta odpowiedzialnego za wykrycie emocji w języku polskim
# Emocje: złość, strach, obrzydzenie, smutek, szczęście, żadna z wymienionych
def return_roberta_emotions_pred(dataframe: pd.DataFrame) -> pd.DataFrame:
    res = predict_file('visegradmedia-emotion/Emotion_RoBERTa_polish6', dataframe)  # predykcje
    res.rename(columns={'LABEL_0': 'anger', 'LABEL_1': 'fear', 'LABEL_3': 'sadness', 'LABEL_4': 'joy'}, inplace=True)  # zmiana nazewnictwa zwracanych wyników
    res.drop(columns=['LABEL_2', 'LABEL_5'], axis=1, inplace=True)  # usunięcie niepotrzebnych etykiet

    columns = ['joy', 'fear', 'sadness', 'anger']
    res = res[columns]
    res = pd.DataFrame(np.argmax(res.to_numpy(), axis=1), columns=['emotion'])

    return res


# Predykcje modelu Roberta odpowiedzialnego za wykrycie depresji w języku angielskim
# Klasy: posiada depresję, nie posiada depresji
def return_en_depression(dataframe: pd.DataFrame) -> pd.DataFrame:
    res = predict_file('ShreyaR/finetuned-roberta-depression', dataframe)  # predykcje
    res.loc[res['LABEL_1'] > res['LABEL_0'], 'en_depress'] = 1  # wskazanie etykiet depresji
    res.loc[res['LABEL_1'] <= res['LABEL_0'], 'en_depress'] = 0
    res['en_depress'] = res['en_depress'].astype(int)
    res.drop(columns=['LABEL_0', 'LABEL_1'], axis=1, inplace=True)  # usunięcie niepotrzebnych etykiet

    return res


# Predykcje modeli GPT2 odpowiedzialnych za analizę sentymentu w zbiorze polskim
# Sentyment: negatywny, pozytywny, neutralny, dwuznaczny
def return_gpt2_pred(dataframe: pd.DataFrame) -> pd.DataFrame:
    gpt2_large = predict_file('nie3e/sentiment-polish-gpt2-large', dataframe) # predykcje
    gpt2_small = predict_file('nie3e/sentiment-polish-gpt2-small', dataframe)
    gpt2_large.drop(columns=['AMBIGUOUS', 'NEUTRAL'], axis=1, inplace=True)  # usunięcie niepotrzebnych etykiet
    gpt2_small.drop(columns=['AMBIGUOUS', 'NEUTRAL'], axis=1, inplace=True)

    layer_soft = torch.nn.Softmax(dim=1)  # wykorzystanie softmax, aby wyrównać wartości sentymentu po usunięcie 2 innych klas

    gpt2_large = pd.DataFrame(layer_soft(torch.tensor(gpt2_large.to_numpy())).detach().numpy(), columns=gpt2_large.columns)
    gpt2_small = pd.DataFrame(layer_soft(torch.tensor(gpt2_large.to_numpy())).detach().numpy(), columns=gpt2_large.columns)

    gpt2_pred = gpt2_large + gpt2_small  # dodanie rezultatów

    gpt2_pred.loc[gpt2_pred['POSITIVE'] > gpt2_pred['NEGATIVE'], 'is_negative'] = 0  # wskazanie etykiet sentymentu
    gpt2_pred.loc[gpt2_pred['POSITIVE'] <= gpt2_pred['NEGATIVE'], 'is_negative'] = 1

    gpt2_pred.drop(columns=['POSITIVE', 'NEGATIVE'], axis=1, inplace=True)   # usunięcie niepotrzebnych etykiet
    gpt2_pred['is_negative'] = gpt2_pred['is_negative'].astype(int)

    return gpt2_pred


# Funkcja łączy rezultaty z modeli:
# 1) analiza sentymentu w wpisach po polsku
# 2) wykrycie emocji w wpisach po polsku
# 3) wykrycie depresji w wpisach przetłumaczonych na język angielski
# Ostatecznie podjęty jest wybór, które podgrupy posiadają depresję na podstawie obliczonych składowych
# Zapisanie predykcji do pliku
def get_polish(dataframe: pd.DataFrame) -> pd.DataFrame:
    gpt2_neg_pos = return_gpt2_pred(dataframe)  # rezultaty GPT2
    roberta_emotion = return_roberta_emotions_pred(dataframe)  # rezultaty RoBERTa dla emocji
    english = pd.read_csv('data/final/polish_translated.csv')
    roberta_en_depress = return_en_depression(english)  # rezultaty RoBERTa dla depresji w języku angielskim

    polish_results = pd.concat([gpt2_neg_pos, roberta_emotion], axis=1)  # złączenie cząstkowych rezultatów
    polish_results = pd.concat([polish_results, roberta_en_depress], axis=1)
    polish_results = pd.concat([dataframe, polish_results], axis=1)

    # wskazanie, które podgrupy danych uznaję za posiadające depresję
    # Grupy:
    # 1) ma negatywny sentyment, posiada depresję po angielsku i smutek z strachem
    # 2) ma pozytywny sentyment, posiada depresję i nie jest zły
    polish_results.loc[(polish_results['is_negative'] == 0) & (polish_results['en_depress'] == 1) & (polish_results['emotion'] != 3), 'label'] = 1
    polish_results.loc[(polish_results['is_negative'] == 1) & (polish_results['en_depress'] == 1) & ((polish_results['emotion'] == 1) | (polish_results['emotion'] == 2)), 'label'] = 1

    polish_results.fillna(0, inplace=True)
    polish_results['label'] = polish_results['label'].astype(int)

    polish_results.drop(columns=['emotion', 'is_negative', 'en_depress'], inplace=True)  # usunięcie niepotrzebnych danych
    polish_results.dropna(inplace=True)
    polish_results.to_csv('data/pl/train_polish.csv', index=False)  # zapis ostatecznego zbioru
    polish_results.reset_index(inplace=True)

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
        else pd.read_csv(os.path.join('data', 'final', 'train_preprocessed_polish.csv')),
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
        output_dir=model_path,
        learning_rate=2e-5,
        per_device_train_batch_size=32,  # 32 dla bert-large, 64 dla bert-base
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
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics
    )

    trainer.train()

    trainer.push_to_hub()

    logout()


def predict_file(model_path: str, dataframe: pd.DataFrame) -> pd.DataFrame:
    dataset = create_dataset(dataframe, split_train_test=False)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    pipe = TextClassificationPipeline(
        model=model,
        tokenizer=tokenizer,
        top_k=None,
        device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    )

    try:
        predictions = prepare_predictions(pipe(dataset['test']['text']), dataframe.index)

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

    return predictions


def prepare_predictions(pred, df_index) -> pd.DataFrame:
    return pd.DataFrame([{pair['label']: pair['score'] for pair in row} for row in pred], index=df_index)


# fine_tune('depression-detect/bert-base')
# fine_tune('depression-detect/bert-large')
# fine_tune('roberta-base')
# fine_tune('roberta-large')

# Wygenerowanie otagowanego zbioru polskiego
# train_polish = get_polish(merge_datasets('pl', False))

# Przetworzone wpisy w obu językach (zbiór treningowy/walidacyjny)
# train_preprocessed_english_dataset = preprocess_dataset(merge_datasets(lang='en', for_train=True), lang='en')
# train_preprocessed_english_dataset.to_csv(os.path.join('data', 'final', 'train_preprocessed_english.csv'), index=False)

train_preprocessed_polish_dataset = preprocess_dataset(get_polish(merge_datasets('pl', False)), lang='pl')
train_preprocessed_polish_dataset.to_csv(os.path.join('data', 'final', 'train_preprocessed_polish.csv'), index=False)

# Przetworzone wpisy w języku angielskim (zbiór testowy)
# test_preprocessed_english_dataset = prepare_tweets()
# test_preprocessed_english_dataset.to_csv(os.path.join('data', 'final', 'test_preprocessed_english.csv'), index=False)