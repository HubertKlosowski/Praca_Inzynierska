# https://huggingface.co/docs/transformers/tasks/sequence_classification
import logging
import os
import numpy as np

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from transformers import (BertTokenizer, BertForSequenceClassification,
                          TrainingArguments, Trainer, DataCollatorWithPadding)
from datasets import Dataset, DatasetDict
import pandas as pd
from prepare import standardize_df
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def preprocess(row):
    return tokenizer(row['text'], truncation=True)


def compute_metrics(logits):
    y_pred, y_true = logits
    y_pred = np.argmax(y_pred, axis=1)
    return {'accuracy': accuracy_score(y_true, y_pred)}


def create_dataset(path: str, file: str) -> DatasetDict:
    dataset = pd.read_csv(os.path.join(path, file))
    dataset = standardize_df(dataset)

    x_train, x_test = train_test_split(dataset, test_size=0.3, random_state=4)
    training = pd.DataFrame(x_train, columns=dataset.columns).reset_index(drop=True)
    testing = pd.DataFrame(x_test, columns=dataset.columns).reset_index(drop=True)

    result = DatasetDict()
    result['train'] = Dataset.from_pandas(training)
    result['test'] = Dataset.from_pandas(testing)

    return result


def train(path: str, file: str, model_name: str):
    dataset = create_dataset(path, file)
    tokenized_dataset = dataset.map(preprocess, batched=True)
    id2label = { 0: 'non-depressed', 1: 'depressed' }
    label2id = { 'non-depressed': 0, 'depressed': 1 }

    # zbędne warningi z hugging-face
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        if "transformers" in logger.name.lower():
            logger.setLevel(logging.ERROR)

    model = BertForSequenceClassification.from_pretrained(
        model_name,
        num_labels=2,
        id2label=id2label,
        label2id=label2id
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    training_args = TrainingArguments(
        output_dir='bert_model',
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=2,
        weight_decay=0.01,
        eval_strategy='epoch',
        save_strategy='epoch',
        load_best_model_at_end=True
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


train('data', 'depression_dataset_reddit_cleaned.csv', 'bert-base-uncased')
