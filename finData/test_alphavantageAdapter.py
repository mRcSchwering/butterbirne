# This Python file uses the following encoding: utf-8
import unittest

from finData.alphavantageAdapter import AlphavantageAdapter


class mock(AlphavantageAdapter):

    @classmethod
    def _request(cls, params):
        return params

    @classmethod
    def _extractData(cls, response):
        return response


class Inits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a = mock()

    def test_fullOutputsize(self):
        res = self.a.getData('ticker')
        self.assertEqual('TIME_SERIES_DAILY_ADJUSTED', res['function'])
        self.assertEqual('ticker', res['symbol'])
        self.assertEqual('full', res['outputsize'])

    def test_compactOutputsize(self):
        res = self.a.getData('ticker', outputsize='small')
        self.assertEqual('TIME_SERIES_DAILY_ADJUSTED', res['function'])
        self.assertEqual('ticker', res['symbol'])
        self.assertEqual('compact', res['outputsize'])

    def test_wrongOutputsize(self):
        with self.assertRaises(AttributeError):
            self.a.getData('ticker', outputsize='asd')

    def test_staticCall(self):
        res = mock.getData('ticker')
        self.assertEqual('TIME_SERIES_DAILY_ADJUSTED', res['function'])
        self.assertEqual('ticker', res['symbol'])
        self.assertEqual('full', res['outputsize'])
