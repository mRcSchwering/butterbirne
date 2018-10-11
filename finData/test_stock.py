# This Python file uses the following encoding: utf-8
import unittest

from finData.stock import Stock


class mock(Stock):

    def downloadHistData(self, outputsize):
        self.histData = outputsize


class Inits(unittest.TestCase):

    def test_nameSetIfProvided(self):
        s = mock('ticker', 'name')
        self.assertEqual('ticker', s.ticker)
        self.assertEqual('name', s.name)

    def test_tickerAsName(self):
        s = mock('ticker')
        self.assertEqual('ticker', s.ticker)
        self.assertEqual('ticker', s.name)

    def test_dataDownloaded(self):
        s = mock('ticker')
        self.assertEqual('all', s.histData)

    def test_dataNotDownloaded(self):
        s = mock('ticker', downloadData=False)
        self.assertIsNone(s.histData)

    def test_smallDataDownloaded(self):
        s = mock('ticker', outputsize='small')
        self.assertEqual('small', s.histData)

    def test_wrongOutputSize(self):
        with self.assertRaises(AttributeError):
            mock('ticker', outputsize='asd')
