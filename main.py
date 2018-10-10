import pandas as pd


stock = Stock('MSFT', False)
stock.histData


# TODO sowas wie stock klasse, wo ich zB hist data dran hängen kann
# -> einfacher mehrere stocks im loop zu laden

from finData.alphavantageAdapter import AlphavantageAdapter


class Stock(object):
    """
    Getting and storing info about stock

    downloadData=True (default) to download upon initializing object
    outputsize='full' (default) to download all data, 'compact' for reduced amount
    """

    tickerSymbol = ''
    histData = None
    _histOutputsize = ''

    def __init__(self, tickerSymbol, downloadData=True, outputsize='full'):
        self.tickerSymbol = tickerSymbol
        self._outputsize = outputsize
        if downloadData:
            self.downloadHistData()

    def downloadHistData(self):
        adapter = AlphavantageAdapter
        self.histData = adapter.getData(self.tickerSymbol, self._outputsize)
