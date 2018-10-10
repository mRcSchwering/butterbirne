# This Python file uses the following encoding: utf-8
from finData.alphavantageApi import AlphavantagApi
from finData.alphavantageConverter import AlphavantageConverter


class AlphavantageAdapter(object):

    @classmethod
    def getData(cls, tickerSymbol, outputsize='full'):
        """
        Get historic data for ticker symbol

        Outputsize can be 'compact' for the last 100 entries
        or 'full' (default) for all data.
        """
        api = AlphavantagApi()
        converter = AlphavantageConverter()
        params = {
            'function': 'TIME_SERIES_DAILY_ADJUSTED',
            'symbol': tickerSymbol,
            'outputsize': outputsize
        }
        resp = api.request(params)
        return converter.responseToDataFrame(resp)
