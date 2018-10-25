# This Python file uses the following encoding: utf-8
import unittest
import pandas as pd
from finData.utils import Utils


class utilsOnHistData(unittest.TestCase):

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
