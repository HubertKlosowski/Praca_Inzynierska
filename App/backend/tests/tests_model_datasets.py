from rest_framework.test import APITestCase
import pandas as pd
import os
from model.model_datasets import create_dataset, balance_dataframe
from datasets import DatasetDict


class TestModelDatasets(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.d1 = pd.read_csv(os.path.join('model', 'data', 'en', 'train', 'depression_dataset_reddit_cleaned.csv'))
        cls.d2 = pd.read_csv(os.path.join('model', 'data', 'en', 'train', 'dataset.csv'))
        cls.d1_shape = cls.d1.shape[0]
        cls.d2_shape = cls.d2.shape[0]

    def test_create_dataset_true(self):
        dataset = create_dataset(self.d1, split_train_test=True)

        self.assertIsInstance(dataset, DatasetDict)
        self.assertIn('train', dataset)
        self.assertIn('test', dataset)
        self.assertEqual(self.d1_shape, dataset['train'].num_rows + dataset['test'].num_rows)
        self.assertAlmostEqual(dataset['train'].num_rows / self.d1_shape, 0.7, places=3)
        self.assertAlmostEqual(dataset['test'].num_rows / self.d1_shape, 0.3, places=3)

    def test_create_dataset_false(self):
        dataset = create_dataset(self.d1, split_train_test=False)

        self.assertIsInstance(dataset, DatasetDict)
        self.assertNotIn('train', dataset)
        self.assertIn('test', dataset)
        self.assertEqual(self.d1_shape, dataset['test'].num_rows)

    def test_balance_dataframes_without_labels(self):
        try:
            balance_dataframe(self.d2.drop(columns=['label']))
        except ValueError as e:
            self.assertEqual(str(e), 'Podanego zbioru nie można zbalansować. Brak kolumny \"label\".')

    def test_balance_dataframes_correct(self):
        try:
            balanced = balance_dataframe(self.d2)
            counts = balanced['label'].value_counts()

            self.assertIsInstance(balanced, pd.DataFrame)
            self.assertEqual(counts[0], counts[1])
        except ValueError:
            pass
