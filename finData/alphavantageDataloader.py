# This Python file uses the following encoding: utf-8
from finData.alphavantageApi import AlphavantagApi
from finData.alphavantageConverter import AlphavantageConverter


class AlphavantageDataloader(object):
    """
    Adapter for downloading historic prices for stock.
    Stock needs to have correct "ticker" attribute.
    Outputsize can be 'compact' for the last 100 entries
    or 'full' (default) for all data.
    """

    outputsize = 'full'

    def __init__(self, outputsize='full'):
        if outputsize not in ['full', 'compact']:
            raise AttributeError('outputsize must be "full" or "compact"')
        self.outputsize = outputsize

    def getData(self, stock):
        params = {
            'function': 'TIME_SERIES_DAILY_ADJUSTED',
            'symbol': stock.ticker,
            'outputsize': self.outputsize
        }
        resp = self._request(params)
        return self._extractData(resp)

    @classmethod
    def _request(cls, params):
        api = AlphavantagApi()
        return api.request(params)

    @classmethod
    def _extractData(cls, response):
        converter = AlphavantageConverter()
        return converter.responseToDataFrame(response)
