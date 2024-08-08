from model import BERT
import torch
import os
import pandas as pd
from torch import nn, optim
from transformers import BertTokenizer
from prepare import limit_lang, standardize_df, limit_length
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


seq_length = 128

model = BERT(
    d_model=768,
    d_ff=3072,
    h=12,
    num_layers=12,
    seq_length=seq_length
)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')  # uncased -> nie ma znaczenia wielkość liter
optimizer = optim.Adam(
    model.parameters(),
    lr=1e-3,
)
criterion = nn.CrossEntropyLoss()

training_dataset = pd.read_csv(os.path.join('..', 'data', 'dataset_2.csv'))
training_dataset = standardize_df(training_dataset)
training_dataset = limit_length(training_dataset, seq_length)
# training_dataset = limit_lang(training_dataset)

X, y = training_dataset.drop(columns=['depressed'], axis=1), training_dataset['depressed']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)
X_train = pd.DataFrame(X_train, columns=X.columns)
X_test = pd.DataFrame(X_test, columns=X.columns)

epochs = 5

model.train()
for i in range(epochs):
    epoch_loss = 0
    for index, row in X_train.iterrows():
        single_sentence = tokenizer(
            row['text'],
            return_tensors='pt',
            padding='max_length',
            max_length=seq_length,
            truncation=True,
        )

        y_pred = model(single_sentence['input_ids'], single_sentence['token_type_ids'])

        y_true = torch.zeros(size=(2, ), dtype=torch.float)
        y_true[y.iloc[index]] = 1

        loss = criterion(y_pred[0], y_true)  # tylko output z tokena CLS, czyli pierwszego
        epoch_loss += loss.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f'Epoch: {i}, Loss: {epoch_loss / len(X_train.index)}')


model.eval()
with torch.no_grad():
    y_pred = torch.zeros(size=(X_test.shape[0], ), dtype=torch.float)
    i = 0
    for index, row in X_test.iterrows():
        single_sentence = tokenizer(
            row['text'],
            return_tensors='pt',
            padding='max_length',
            max_length=seq_length,
            truncation=True
        )

        pred = model(single_sentence['input_ids'], single_sentence['token_type_ids'])
        y_pred[i] = torch.argmax(pred[0], dim=0)
        i += 1

print(classification_report(y_test, y_pred))
