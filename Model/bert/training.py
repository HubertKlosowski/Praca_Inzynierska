from model import BERT
import torch
import math
import os
import pandas as pd
from torch import nn, optim, Tensor
from transformers import BertTokenizer
from prepare import limit_lang, standardize_df, limit_length
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from time import perf_counter
from torch.utils.data import Dataset, DataLoader


class BertDataset(Dataset):
    def __init__(self, input_ids: torch.Tensor, token_type_ids: torch.Tensor, attention_mask: torch.Tensor,
                 labels_proba: torch.Tensor):
        self.input_ids = input_ids
        self.token_type_ids = token_type_ids
        self.attention_mask = attention_mask
        self.labels_proba = labels_proba

    def __len__(self):
        return self.input_ids.shape[0]

    def __getitem__(self, idx):
        sample = {'input_ids': self.input_ids[idx], 'token_type_ids': self.token_type_ids[idx],
                  'attention_mask': self.attention_mask[idx], 'labels_proba': self.labels_proba[idx]}
        return sample


def create_dataset(df: pd.DataFrame, labels: pd.Series) -> tuple[Tensor, Tensor, Tensor, Tensor]:
    input_ids_tensor = torch.zeros(size=(len(df), seq_length), dtype=torch.int, device=device)
    token_type_ids_tensor = torch.zeros(size=(len(df), seq_length), dtype=torch.int, device=device)
    attention_mask_tensor = torch.zeros(size=(len(df), seq_length), dtype=torch.int, device=device)
    labels_proba_tensor = torch.zeros(size=(len(df), 2), dtype=torch.float, device=device)
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
        attention_mask_tensor[index] = single_sentence['attention_mask']
        labels_proba_tensor[index][labels.iloc[index]] = 1.0
    return input_ids_tensor, token_type_ids_tensor, attention_mask_tensor, labels_proba_tensor


def bert_train(input_ids: torch.Tensor, token_type_ids: torch.Tensor, attention_mask: torch.Tensor,
               labels_proba: torch.Tensor, epochs: int = 5, batch_size: int = 256):
    dataset = BertDataset(input_ids, token_type_ids, attention_mask, labels_proba)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=0)

    # Użycie skalowania gradientu w technice AMP zapobiega zanikaniu gradientów o małych wartościach
    scaler = torch.amp.GradScaler('cuda')

    batch_num = math.ceil(input_ids.shape[0] / batch_size)
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        start_epoch_time = perf_counter()  # z ciekawości

        for batch in dataloader:
            start_batch_time = perf_counter()  # z ciekawości

            batch_input_ids = batch['input_ids']
            batch_token_type_ids = batch['token_type_ids']
            batch_attention_mask = batch['attention_mask']
            batch_labels_proba = batch['labels_proba']

            # polecane zamiast optimizer.zero_grad() ze względu na ograniczenie operacji w pamięci
            optimizer.zero_grad(set_to_none=True)

            # Automatic Mixed Precision (AMP) umożliwia wykonanie pewnych operacji przy użyciu FP16, niż FP32 bez straty
            # dokładności w wynikach.
            # Zalety: mniejsze użycie pamięci karty graficznej, szybsze wykonanie operacji
            with torch.autocast(device_type=device, dtype=torch.float16):
                y_pred = model(batch_input_ids, batch_token_type_ids, batch_attention_mask)

                loss = criterion(y_pred, batch_labels_proba)
                epoch_loss += loss.item()

            scaler.scale(loss).backward()  # zamiast loss.backward()
            scaler.step(optimizer)  # zamiast optimizer.step()
            scaler.update()

            print(f'Batch loss: {loss.item()}, Time: {round(perf_counter() - start_batch_time, 2)}s')
        print(f'Epoch: {epoch}, Loss: {epoch_loss / batch_num}, Time: {round(perf_counter() - start_epoch_time, 2)}s')


def bert_test(input_ids: torch.Tensor, token_type_ids: torch.Tensor, attention_mask: torch.Tensor, y_true: torch.Tensor):
    model.eval()
    with torch.no_grad():
        y_pred = model(input_ids, token_type_ids, attention_mask)
        y_pred = y_pred.squeeze().argmax(dim=1).numpy(force=True)
    print(classification_report(y_true, y_pred))


if __name__ == '__main__':
    seq_length = 128
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
    optimizer = optim.AdamW(
        model.parameters(),
        lr=1e-5,
        betas=(0.9, 0.99)
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

    train_input_ids, train_token_type_ids, train_attention_mask, train_label_proba = create_dataset(X_train, y_train)
    test_input_ids, test_token_type_ids, test_attention_mask, test_label_proba = create_dataset(X_test, y_test)

    bert_train(train_input_ids, train_token_type_ids, train_attention_mask, train_label_proba)

    torch.save(model.state_dict(), os.path.join('..', 'data', 'custom-bert-base.pt'))

    bert_test(test_input_ids, test_token_type_ids, test_attention_mask, torch.tensor(y_test.values))
