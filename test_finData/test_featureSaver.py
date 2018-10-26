# This Python file uses the following encoding: utf-8
import unittest
from finData.featureSaver import FeatureSaver
import pandas as pd
import tempfile


class MockStock(object):

    def __init__(self):
        self.isin = 'isin'
        self.features = pd.read_pickle('testdata/histFeatures_MMM.pkl')


class MakeLong(unittest.TestCase):

    def test_longStructure(self):
        wide = MockStock().features
        res = FeatureSaver._makeLong(wide)
        exp = ['month', 'year', 'variable', 'value']
        self.assertSetEqual(set(exp), set(res.columns))
        exp = ['logReturn', 'vola']
        self.assertSetEqual(set(exp), set(res['variable'].tolist()))
        self.assertSetEqual(set([2018]), set(res['year'].tolist()))
        self.assertSetEqual(set([9, 8, 7, 6]), set(res['month'].tolist()))
        self.assertEqual(
            wide.loc[wide['month'] == 9].at[0, 'vola'],
            res.loc[(res['month'] == 9) & (res['variable'] == 'vola'), 'value'].iat[0]
        )
        self.assertEqual(
            wide.loc[wide['month'] == 9].at[0, 'logReturn'],
            res.loc[(res['month'] == 9) & (res['variable'] == 'logReturn'), 'value'].iat[0]
        )

    def test_longStructureWithRepeatingIds(self):
        df = pd.DataFrame({
            'month': [1, 1],
            'year': [1, 1],
            'feature1': [1, 1]
        })
        res = FeatureSaver._makeLong(df)
        exp = ['month', 'year', 'variable', 'value']
        self.assertSetEqual(set(exp), set(res.columns))
        self.assertListEqual(['feature1', 'feature1'], res['variable'].tolist())
        for col in ['month', 'year', 'value']:
            self.assertListEqual([1, 1], res[col].tolist())


class AddIsin(unittest.TestCase):

    def test_isinAdded(self):
        res = FeatureSaver._addIsin(pd.DataFrame({'a': [1, 2]}), 'b')
        self.assertSetEqual(set(['isin', 'a']), set(res.columns))
        self.assertSetEqual(set(['b']), set(res['isin'].tolist()))


class WriteOutfile(unittest.TestCase):

    def test_newFileCreated(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = '%s/file' % tmp
            df = pd.DataFrame({'a': [1, 2], 'b': [11, 22]})
            FeatureSaver._writeOutfile(df, file)
            res = pd.read_csv(file)
        self.assertListEqual(['a', 'b'], res.columns.tolist())

    def test_existingFileAppended(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = '%s/file' % tmp
            df = pd.DataFrame({'a': [1, 2], 'b': [11, 22]})
            FeatureSaver._writeOutfile(df, file)
            df = pd.DataFrame({'a': [3, 4], 'b': [33, 44]})
            FeatureSaver._writeOutfile(df, file)
            res = pd.read_csv(file)
        self.assertListEqual(['a', 'b'], res.columns.tolist())
        self.assertListEqual([1, 2, 3, 4], res['a'].tolist())
        self.assertListEqual([11, 22, 33, 44], res['b'].tolist())

    def test_columnsAreNotMatching(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = '%s/file' % tmp
            df = pd.DataFrame({'a': [1, 2], 'b': [11, 22]})
            FeatureSaver._writeOutfile(df, file)
            df = pd.DataFrame({'c': [33, 44], 'a': [3, 4]})
            with self.assertRaises(AttributeError):
                FeatureSaver._writeOutfile(df, file)

    def test_columnsHaveToBeReordered(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = '%s/file' % tmp
            df = pd.DataFrame({'a': [1, 2], 'b': [11, 22]})
            FeatureSaver._writeOutfile(df, file)
            df = pd.DataFrame({'b': [33, 44], 'a': [3, 4]})
            FeatureSaver._writeOutfile(df, file)
            res = pd.read_csv(file)
        self.assertListEqual(['a', 'b'], res.columns.tolist())
        self.assertListEqual([1, 2, 3, 4], res['a'].tolist())
        self.assertListEqual([11, 22, 33, 44], res['b'].tolist())


class WriteFeatures(unittest.TestCase):

    def test_writeNewFeatures(self):
        stock = MockStock()
        with tempfile.TemporaryDirectory() as tmp:
            file = '%s/file' % tmp
            f = FeatureSaver(file)
            f.writeFeatures(stock)
            res = pd.read_csv(file)
        self.assertTupleEqual((8, 5), res.shape)
        self.assertSetEqual(set(['isin']), set(res['isin']))
        self.assertSetEqual(set([2018]), set(res['year']))
        self.assertSetEqual(set([9, 8, 7, 6]), set(res['month']))
        self.assertSetEqual(set(['logReturn', 'vola']), set(res['variable']))

    def test_appendUnorderedFeatures(self):
        stock = MockStock()
        with tempfile.TemporaryDirectory() as tmp:
            file = '%s/file' % tmp
            f = FeatureSaver(file)
            f.writeFeatures(stock)
            cols = ['logReturn', 'year', 'vola', 'month']
            stock.features = stock.features[cols]
            f.writeFeatures(stock)
            res = pd.read_csv(file)
        self.assertTupleEqual((16, 5), res.shape)
        self.assertSetEqual(set(['isin']), set(res['isin']))
        self.assertSetEqual(set([2018]), set(res['year']))
        self.assertSetEqual(set([9, 8, 7, 6]), set(res['month']))
        self.assertSetEqual(set(['logReturn', 'vola']), set(res['variable']))
