import os
import re
from concurrent.futures import ThreadPoolExecutor

from langdetect import DetectorFactory

DetectorFactory.seed = 0

import numpy as np
import spacy
import torch
from datasets import Dataset, DatasetDict
from googletrans import Translator
from nltk.stem import PorterStemmer  # stemming dla języka angielskiego
from sklearn.model_selection import train_test_split

from model.api_keys import save_model_token

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from transformers import (AutoModelForSequenceClassification, TextClassificationPipeline,
                          TrainingArguments, Trainer, DataCollatorWithPadding, AutoTokenizer)
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from huggingface_hub import login, logout


def detect_lang(df: pd.DataFrame) -> str:
    translator = Translator(service_urls=[
      'translate.googleapis.com'
    ])
    df['text'] = df['text'].apply(lambda x: x.strip())

    def detect_language(row: str) -> str:
        return translator.detect(row).lang

    with ThreadPoolExecutor(max_workers=20) as executor:
        langs = executor.map(detect_language, df['text'].values)

    df['lang'] = np.array([l for l in langs], dtype=str)
    counts = df['lang'].value_counts()
    df.drop(columns=['lang'], inplace=True)
    return counts.idxmax(axis=0)

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

# Połączenie zbiorów w jeden
def merge_dataframes(for_train: bool = False) -> pd.DataFrame:
    merged = pd.DataFrame()
    columns = ['text', 'label'] if for_train else ['text']
    path = os.path.join(os.path.join('model', 'data', 'en', 'train')) if for_train \
        else os.path.join(os.path.join('model', 'data', 'en', 'test'))

    for d in os.listdir(path):
        dataframe = pd.read_csv(os.path.join(path, d))
        dataframe = dataframe[columns].reset_index(drop=True)
        merged = pd.concat([merged, dataframe], axis=0)

    merged.drop_duplicates(subset=['text'], keep='first', inplace=True)  # usuniecie duplikatow
    merged.dropna(inplace=True)  # usuniecie wartosci NaN
    merged['text'] = merged['text'].apply(lambda x: x.replace('\n', ' '))
    merged['len'] = merged['text'].apply(lambda x: len(x.split()))
    merged.drop(merged.loc[
                    (merged['len'] <= merged['len'].quantile(0.04)) |
                    (merged['len'] >= merged['len'].quantile(0.94))].index, inplace=True
                )
    merged.drop(columns=['len'], inplace=True)
    merged.reset_index(drop=True, inplace=True)

    return merged

def balance_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    if 'label' not in dataframe.columns:
        raise ValueError('Podanego zbioru nie można zbalansować. Brak kolumny \"label\".')

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
def preprocess_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    lang_resource = spacy.load('en_core_web_sm')
    lang_resource.add_pipe('emoji', first=True)

    stemmer = PorterStemmer()

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
    dataframe['text'] = dataframe['text'].apply(
        lambda tokens: [token._.emoji_desc if token._.is_emoji else token.text for token in tokens]
    )
    dataframe['text'] = dataframe['text'].apply(lambda tokens: [stemmer.stem(token) for token in tokens])
    dataframe['text'] = dataframe['text'].apply(
        lambda tokens: ' '.join([str(token) for token in tokens if token is not None])
    )

    dataframe['len'] = dataframe['text'].str.len()
    dataframe.drop(index=dataframe.loc[dataframe['len'] == 0, :].index, inplace=True)
    dataframe.drop(columns=['len'], inplace=True)

    return dataframe

# obsluga zbyt dlugich wpisow
def drop_too_long(df: pd.DataFrame, tokenizer) -> pd.DataFrame:
    df_copy = df.copy(deep=True)
    limit = 500
    df_copy['len'] = df_copy['text'].apply(lambda sentence: len(tokenizer.tokenize(sentence)))
    df_copy.drop(df_copy.loc[df_copy['len'] > limit, ['text']].index, inplace=True)  # wpisy zbyt dlugie
    df_copy.drop(columns=['len'], inplace=True)
    return df_copy

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
        pd.read_csv(os.path.join('data', 'final', 'train_preprocessed_english.csv')),
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
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
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

def predict(model_path: str, dataframe: pd.DataFrame, truncate: bool = True, login_token: str = None) -> pd.DataFrame:
    if login_token is not None:
        login(token=login_token)

    dataset = create_dataset(dataframe, split_train_test=False)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    pipe = TextClassificationPipeline(
        model=model,
        tokenizer=tokenizer,
        top_k=None,
        device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    )

    if truncate:
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


# fine_tune('google-bert/bert-base-uncased')
# fine_tune('google-bert/bert-large-uncased')

# Przetworzone wpisy dla języka angielskiego (zbiór treningowy)
# if 'train_english.csv' in os.listdir(os.path.join('data', 'final')):
#     train_english = pd.read_csv(os.path.join('data', 'final', 'train_english.csv'))  # tylko połączony zbiór
# else:
#     train_english = merge_dataframes(lang='en', for_train=True)
#     train_english.to_csv(os.path.join('data', 'final', 'train_english.csv'), index=False)
#
# try:
#     train_english = balance_dataframe(train_english)
#     train_preprocessed_english = preprocess_dataframe(train_english, lang='en')
#     train_preprocessed_english.to_csv(os.path.join('data', 'final', 'train_preprocessed_english.csv'), index=False)
# except ValueError as e:
#     print(str(e))

# Przetworzone wpisy w języku angielskim (zbiór testowy)
# if 'test_english.csv' in os.listdir(os.path.join('data', 'final')):
#     test_preprocessed_english = preprocess_dataframe(pd.read_csv(os.path.join('data', 'final', 'test_english.csv')))
#     test_preprocessed_english.dropna(subset=['text'], inplace=True)
#     test_preprocessed_english.to_csv(os.path.join('data', 'final', 'test_preprocessed_english.csv'), index=False)