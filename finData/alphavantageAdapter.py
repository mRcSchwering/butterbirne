# This Python file uses the following encoding: utf-8
from finData.alphavantageApi import AlphavantagApi
from finData.alphavantageConverter import AlphavantageConverter


class AlphavantageAdapter(object):

    @classmethod
    def getData(cls, tickerSymbol, outputsize='all'):
        """
        Get historic data for ticker symbol

        Outputsize can be 'small' for the last 100 entries
        or 'all' (default) for all data.
        """
        if outputsize not in ['all', 'small']:
            raise AttributeError('outputsize must be "all" or "small"')
        outputsize = 'compact' if outputsize == 'small' else 'full'
        params = {
            'function': 'TIME_SERIES_DAILY_ADJUSTED',
            'symbol': tickerSymbol,
            'outputsize': outputsize
        }
        resp = cls._request(params)
        return cls._extractData(resp)

    @classmethod
    def _request(cls, params):
        api = AlphavantagApi()
        return api.request(params)

    @classmethod
    def _extractData(cls, response):
        converter = AlphavantageConverter()
        return converter.responseToDataFrame(response)
