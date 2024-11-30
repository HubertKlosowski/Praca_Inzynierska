import pandas as pd

test = pd.read_json('final_dataset.json')

test.drop(columns=['title'], inplace=True)

test.to_json('test.json', index=False)