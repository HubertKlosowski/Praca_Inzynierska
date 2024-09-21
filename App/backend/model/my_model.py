# https://huggingface.co/docs/transformers/tasks/sequence_classification
import logging
import os
import numpy as np
import torch

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from transformers import (AutoModelForSequenceClassification, TextClassificationPipeline,
                          TrainingArguments, Trainer, DataCollatorWithPadding, AutoTokenizer)
from datasets import Dataset, DatasetDict
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split


def preprocess(tokenizer, row):
    return tokenizer(row['text'], truncation=True)


def compute_metrics(logits):
    y_pred, y_true = logits
    y_pred = np.argmax(y_pred, axis=1)
    return {'accuracy': accuracy_score(y_true, y_pred)}


def create_dataset(dataset: pd.DataFrame, split_train_test: bool) -> DatasetDict:
    dt = DatasetDict()

    if split_train_test:
        x_train, x_test = train_test_split(dataset, test_size=0.3, random_state=4)
        training = pd.DataFrame(x_train, columns=dataset.columns).reset_index(drop=True)
        testing = pd.DataFrame(x_test, columns=dataset.columns).reset_index(drop=True)

        dt['train'] = Dataset.from_pandas(training)
        dt['test'] = Dataset.from_pandas(testing)

    else:
        dt['test'] = Dataset.from_pandas(dataset)
    return dt


def train(path: str, file: str, model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    dataset = create_dataset(
        pd.read_csv(os.path.join(path, file)),
        split_train_test=True
    )
    tokenized_dataset = dataset.map(lambda x: preprocess(tokenizer, x), batched=True)
    id2label = { 0: 'non-depressed', 1: 'depressed' }
    label2id = { 'non-depressed': 0, 'depressed': 1 }

    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=2,
        id2label=id2label,
        label2id=label2id
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    training_args = TrainingArguments(
        output_dir=f'{model_name}-directory',
        learning_rate=2e-5,
        per_device_train_batch_size=64,
        per_device_eval_batch_size=64,
        num_train_epochs=2,
        weight_decay=0.01,
        eval_strategy='epoch',
        save_strategy='epoch',
        load_best_model_at_end=True,
        log_level='error'
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

    trainer.save_model(f'saved-{model_name}')


def predict(model_path: str, model_name: str, data: DatasetDict) -> dict:
    model = AutoModelForSequenceClassification.from_pretrained(os.path.join(model_path))
    tokenizer = AutoTokenizer.from_pretrained(model_name, truncation=True, max_length=512)

    pipe = TextClassificationPipeline(
        model=model,
        tokenizer=tokenizer,
        top_k=None,
        device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    )

    predictions = pipe(data['test']['text'])

    for i, row in enumerate(predictions):
        predictions[i] = max(row, key=lambda x: x['score'])

    predictions = pd.DataFrame(predictions)
    predictions['label_id'] = predictions['label'].map({ 'non-depressed': 0, 'depressed': 1 })

    metrics = {
        'accuracy': accuracy_score(y_true=data['test']['label'], y_pred=predictions['label_id']),
        'recall': recall_score(y_true=data['test']['label'], y_pred=predictions['label_id']),
        'precision': precision_score(y_true=data['test']['label'], y_pred=predictions['label_id']),
        'f1-score': f1_score(y_true=data['test']['label'], y_pred=predictions['label_id'])
    }

    matrix = confusion_matrix(y_true=data['test']['label'], y_pred=predictions['label_id'])

    return {
        'metrics': metrics,
        # 'predictions': predictions,
        'confusion_matrix': matrix
    }


# train('data', 'depression_dataset_reddit_cleaned.csv', 'bert-base-uncased')
# train('data', 'depression_dataset_reddit_cleaned.csv', 'bert-large-uncased')