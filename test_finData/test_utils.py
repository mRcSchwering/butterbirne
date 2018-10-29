# This Python file uses the following encoding: utf-8
import unittest
import pandas as pd
from finData.utils import Utils


class UtilsOnHistData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_pickle('testdata/histData_MMM.pkl')

    def test_filterByMonth(self):
        df = Utils.filterBy(self.df, month=7, year=2018)
        for d in df.index:
            self.assertEqual(7, d.month)
        for i in range(1, df.shape[0]):
            self.assertGreater(df.index[i], df.index[i-1])
        df = Utils.filterBy(self.df, month=9, year=2018)
        for d in df.index:
            self.assertEqual(9, d.month)
        for i in range(1, df.shape[0]):
            self.assertGreater(df.index[i], df.index[i-1])

    def test_filterByMonthReturnsEmpty(self):
        df = Utils.filterBy(self.df, month=1, year=2018)
        self.assertEqual(0, df.shape[0])
        df = Utils.filterBy(self.df, month=9, year=2017)
        self.assertEqual(0, df.shape[0])


class CheckStockInfo(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'a': ['a', 'b'], 'b': ['c', 'd']})

    def test_wrongTypeProvided(self):
        with self.assertRaises(TypeError):
            Utils.checkStockInfo('asd', ['a'])
        with self.assertRaises(TypeError):
            Utils.checkStockInfo(self.df, 'a')
        Utils.checkStockInfo(self.df, ['a'])

    def test_columnMissing(self):
        with self.assertRaises(AttributeError):
            Utils.checkStockInfo(self.df, ['c'])
        Utils.checkStockInfo(self.df, ['a', 'b'])

    def test_missingValues(self):
        self.df.iat[0, 0] = ''
        with self.assertRaises(ValueError):
            Utils.checkStockInfo(self.df, ['a', 'b'])
