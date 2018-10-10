# This Python file uses the following encoding: utf-8
import unittest
import pandas as pd

from finData.alphavantageConverter import AlphavantageConverter


class getMapping(unittest.TestCase):

    def test_mapping(self):
        converter = AlphavantageConverter()
        self.assertIsInstance(converter._mapping, list)


class createDataFrame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.converter = AlphavantageConverter()

    def test_fromRecordLikeStructure(self):
        data = {
            '2011': {'b': 1, 'c': 2},
            '2012': {'b': 3, 'c': 4},
        }
        df = self.converter._createDataFrame(data)
        self.assertIsInstance(df, pd.core.frame.DataFrame)
        idx = df.index
        self.assertTupleEqual((2, 2), df.shape)
        self.assertIsInstance(idx, pd.core.indexes.datetimes.DatetimeIndex)

    def test_correctOrder(self):
        data = {
            '2011': {'b': 1, 'c': 2},
            '2012': {'b': 3, 'c': 4},
        }
        df = self.converter._createDataFrame(data)
        idx = [str(d.date()) for d in df.index]
        self.assertListEqual(['2011-01-01', '2012-01-01'], idx)
        self.assertEqual(1, df.iat[0, 0])
        self.assertEqual(2, df.iat[0, 1])
        self.assertEqual(3, df.iat[1, 0])
        self.assertEqual(4, df.iat[1, 1])

    def test_errorIfCannotCreateIndex(self):
        data = {'a': {'b': 1, 'c': 2}}
        with self.assertRaises(ValueError):
            self.converter._createDataFrame(data)


class customizeDataFrame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.converter = AlphavantageConverter()
        cls.converter._mapping = [
            {'from': 'as', 'to': 'AS'},
            {'from': 'de', 'to': 'DE'},
            {'from': 'fg', 'to': 'FG'},
            {'from': 'fgg', 'to': 'FGG'}
        ]

    def test_notAllMapsInColumns(self):
        df = pd.DataFrame({'fg': [3, 4], 'de': [1, 2]})
        res = self.converter._customizeDataFrame(df)
        self.assertListEqual([3, 4], res['FG'].tolist())
        self.assertListEqual([1, 2], res['DE'].tolist())

    def test_nonExactColumnNames(self):
        df = pd.DataFrame({'xnlfg': [3, 4], 'dexnl': [1, 2]})
        res = self.converter._customizeDataFrame(df)
        self.assertListEqual([3, 4], res['FG'].tolist())
        self.assertListEqual([1, 2], res['DE'].tolist())

    def test_stringsBecomeNumbers(self):
        df = pd.DataFrame({'fg': ['3', '4'], 'de': ['1', '2']})
        res = self.converter._customizeDataFrame(df)
        self.assertListEqual([3, 4], res['FG'].tolist())
        self.assertListEqual([1, 2], res['DE'].tolist())

    def test_if2matchesTakeLongerOne(self):
        df = pd.DataFrame({'fg': [3, 4], 'fgg': [1, 2]})
        res = self.converter._customizeDataFrame(df)
        self.assertListEqual([3, 4], res['FG'].tolist())
        self.assertListEqual([1, 2], res['FGG'].tolist())


class responseToDataFrame(unittest.TestCase):

    def test_noTimeSeriesThrowsError(self):
        converter = AlphavantageConverter()
        with self.assertRaises(KeyError):
            converter.responseToDataFrame({'a': 1})
