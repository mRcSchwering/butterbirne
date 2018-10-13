# This Python file uses the following encoding: utf-8


class Stock(object):
    """
    Getting and storing info about stock
    """

    ticker = ''
    isin = ''
    name = ''
    data = None

    def __init__(self, isin, name='', ticker=''):
        self.isin = isin
        self.ticker = ticker
        self.name = isin if name == '' else name

    def loadData(self, dataloader):
        """
        Provide adapter for downloading data for this stock.
        """
        self.data = dataloader.getData(self)
