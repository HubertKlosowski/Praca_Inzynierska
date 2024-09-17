import pandas as pd
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


# nltk.download('punkt')
# nltk.download('stopwords')


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


def standardize_df(df: pd.DataFrame) -> pd.DataFrame:
    columns = ['text', 'label']  # zmiana nazw kolumn
    for i, column in enumerate(df.columns):
        df.rename(columns={column: columns[i]}, inplace=True)

    df.dropna(inplace=True)  # usunięcie wartości NaN
    df['label'] = df['label'].astype(int)
    return df
