# This Python file uses the following encoding: utf-8
import unittest

from finData.alphavantageDataloader import AlphavantageDataloader


class mock(AlphavantageDataloader):

    @classmethod
    def _request(cls, params):
        return params

    @classmethod
    def _extractData(cls, response):
        return response


class stock(object):

    ticker = 'ticker'


class GetData(unittest.TestCase):

    def test_staticCall(self):
        res = mock().getData(stock)
        self.assertEqual('TIME_SERIES_DAILY_ADJUSTED', res['function'])
        self.assertEqual('ticker', res['symbol'])
        self.assertEqual('full', res['outputsize'])

    def test_failsIfNoTicker(self):
        with self.assertRaises(AttributeError):
            mock().getData('')

    def test_wrongOutputsize(self):
        with self.assertRaises(AttributeError):
            mock('asd').getData(stock)

    def test_smallOutputsize(self):
        res = mock('compact').getData(stock)
        self.assertEqual('TIME_SERIES_DAILY_ADJUSTED', res['function'])
        self.assertEqual('ticker', res['symbol'])
        self.assertEqual('compact', res['outputsize'])
