# This Python file uses the following encoding: utf-8
from finData.alphavantageAdapter import AlphavantageAdapter


class Stock(object):
    """
    Getting and storing info about stock

    downloadData=True (default) to download upon initializing object
    outputsize='all' (default) to download all data, 'small' for reduced amount
    """

    ticker = ''
    histData = None
    name = ''
    volatility = {'daily': None, 'monthly': None, 'yearly': None}
    _histOutputsize = ''

    def __init__(self, ticker, name='', downloadData=True, outputsize='all'):
        if outputsize not in ['all', 'small']:
            raise AttributeError('outputsize must be "all" or "small"')
        self.ticker = ticker
        self.name = ticker if name == '' else name
        self._outputsize = outputsize
        if downloadData:
            self.downloadHistData(self._outputsize)

    def downloadHistData(self, outputsize):
        adapter = AlphavantageAdapter
        self.histData = adapter.getData(self.ticker, outputsize)
