import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import os


def depression_literature(request):
    soup = BeautifulSoup(request.content, 'html.parser')
    all_p = soup.find_all('p', class_='')
    return [element.get_text() for element in all_p]


def polish_test_depression_literature():
    posts = []
    urls = [f'https://lubimyczytac.pl/cytaty/t/depresja?page={i}&listId=quoteListFull&tags%5B0%5D=depresja&tags%5B1%5D=depresja&showFirstLetter=0&paginatorType=Standard&paginatorType=Standard' for i in range(84)]

    with ThreadPoolExecutor(max_workers=10) as executor:
        res = [executor.submit(depression_literature, requests.get(url)) for url in urls]
        for f in as_completed(res):
            posts.append(f.result())

    depress_literature = pd.DataFrame()
    for row in posts:
        depress_literature = pd.concat([depress_literature, pd.DataFrame(row)], axis=0, ignore_index=True)

    depress_literature.rename(columns={depress_literature.columns[0]: 'text'}, inplace=True)
    depress_literature['text'] = depress_literature['text'].apply(lambda x: x.strip())
    depress_literature['text'] = depress_literature['text'].apply(lambda x: x.replace('\n', ' '))
    depress_literature['text'] = depress_literature['text'].apply(lambda x: x.replace('(...)', ''))
    depress_literature['text'] = depress_literature['text'].apply(lambda x: x.replace('[...]', ''))
    depress_literature.drop_duplicates(inplace=True)
    depress_literature.reset_index(drop=True, inplace=True)
    depress_literature.to_csv(os.path.join('data', 'pl', 'test', 'depress_literature.csv'), index=False)

    return depress_literature


def polish_test_jokes():
    polish_jokes = pd.read_parquet(
        'hf://datasets/JonaszPotoniec/dowcipy-polish-jokes-dataset/data/train-00000-of-00001.parquet')

    polish_jokes = polish_jokes[['joke']]
    polish_jokes.rename(columns={'joke': 'text'}, inplace=True)
    polish_jokes['len'] = polish_jokes['text'].apply(lambda x: len(x.split()))
    polish_jokes = polish_jokes.loc[polish_jokes['len'] < 300, :].copy(deep=True)
    polish_jokes['text'] = polish_jokes['text'].apply(lambda x: x.strip())
    polish_jokes['text'] = polish_jokes['text'].apply(lambda x: x.replace('\n', ' '))
    polish_jokes.drop(columns=['len'], inplace=True)
    polish_jokes.drop_duplicates(inplace=True)
    polish_jokes.reset_index(drop=True, inplace=True)
    polish_jokes.to_csv(os.path.join('data', 'pl', 'test', 'polish_jokes.csv'), index=False)

    return polish_jokes

polish_test_jokes()