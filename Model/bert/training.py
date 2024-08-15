from model import BERT
import torch
import math
import os
import pandas as pd
from torch import nn, optim
from transformers import BertTokenizer
from prepare import limit_lang, standardize_df, limit_length
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from time import perf_counter


def create_dataset(df: pd.DataFrame, labels: pd.Series) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    input_ids_tensor = torch.zeros(size=(len(df), seq_length))
    token_type_ids_tensor = torch.zeros(size=(len(df), seq_length))
    labels_proba_tensor = torch.zeros(size=(len(df), 2), dtype=torch.long)
    for index, row in df.iterrows():
        single_sentence = tokenizer(
            row['text'],
            return_tensors='pt',
            padding='max_length',
            max_length=seq_length,
            truncation=True,
        )
        input_ids_tensor[index] = single_sentence['input_ids']
        token_type_ids_tensor[index] = single_sentence['token_type_ids']
        labels_proba_tensor[index][labels.iloc[index]] = 1
    return (input_ids_tensor.to(dtype=torch.int, device=device),
            token_type_ids_tensor.to(dtype=torch.int, device=device),
            labels_proba_tensor.to(dtype=torch.float, device=device))


def bert_train(input_ids: torch.Tensor, token_type_ids: torch.Tensor, labels_proba: torch.Tensor, epochs: int = 5,
               batch_size: int = 256):
    batch_num = math.ceil(input_ids.shape[0] / batch_size)
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0
        start_epoch_time = perf_counter()  # z ciekawości

        for batch_idx in range(batch_num):
            start_batch_time = perf_counter()  # z ciekawości

            batch_input_ids = input_ids[batch_idx * batch_size:(batch_idx + 1) * batch_size, :]
            batch_token_type_ids = token_type_ids[batch_idx * batch_size:(batch_idx + 1) * batch_size, :]
            batch_labels_proba = labels_proba[batch_idx * batch_size:(batch_idx + 1) * batch_size, :]

            optimizer.zero_grad()
            y_pred = model(batch_input_ids, batch_token_type_ids)

            loss = criterion(y_pred, batch_labels_proba)
            epoch_loss += loss.item()
            loss.backward()
            optimizer.step()
            print(f'Batch loss: {loss.item()}, Time: {round(perf_counter() - start_batch_time, 2)}s')

        print(f'Epoch: {epoch}, AVG Loss: {epoch_loss / batch_num}, Time: {round(perf_counter() - start_epoch_time, 2)}s')


def bert_test(input_ids: torch.Tensor, token_type_ids: torch.Tensor, y_true: torch.Tensor):
    model.eval()
    with torch.no_grad():
        y_pred = model(input_ids, token_type_ids)
        y_pred = y_pred.squeeze().argmax(dim=1).numpy(force=True)
    print(classification_report(y_true, y_pred))


if __name__ == '__main__':
    seq_length = 256
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    model = BERT(
        d_model=768,
        d_ff=3072,
        h=12,
        num_layers=12,
        seq_length=seq_length,
        device=device
    ).to(device=device)

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')  # uncased -> nie ma znaczenia wielkość liter
    optimizer = optim.Adam(
        model.parameters(),
        lr=1e-3,
    )
    criterion = nn.CrossEntropyLoss()

    training_dataset = pd.read_csv(os.path.join('..', 'data', 'depression_dataset_reddit_cleaned.csv'))
    training_dataset = standardize_df(training_dataset)
    training_dataset = limit_length(training_dataset, seq_length)
    # training_dataset = limit_lang(training_dataset)

    X, y = training_dataset.drop(columns=['depressed'], axis=1), training_dataset['depressed']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4)
    X_train = pd.DataFrame(X_train, columns=X.columns).reset_index(drop=True)
    X_test = pd.DataFrame(X_test, columns=X.columns).reset_index(drop=True)

    train_input_ids, train_token_type_ids, train_label_proba = create_dataset(X_train, y_train)
    test_input_ids, test_token_type_ids, test_label_proba = create_dataset(X_test, y_test)

    bert_train(train_input_ids, train_token_type_ids, train_label_proba)

    bert_test(test_input_ids, test_token_type_ids, torch.tensor(y_test.values))
