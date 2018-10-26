# This Python file uses the following encoding: utf-8


class Stock(object):
    """
    Getting and storing info about stock
    """

    ticker = ''
    isin = ''
    name = ''
    data = None
    features = None

    def __init__(self, isin, name='', ticker=''):
        self.isin = isin
        self.ticker = ticker
        self.name = isin if name == '' else name

    def loadData(self, dataloader):
        """
        Provide adapter for downloading data for this stock.
        """
        self.data = dataloader.getData(self)

    def extractFeatures(self, extractor):
        """
        Provide adapter for extracting features for this data.
        """
        if self.data is None:
            raise AttributeError('Stock has no data, loadData first')
        self.features = extractor.getFeatures(self)

    def saveFeatures(self, writer):
        """
        Provide adapter for saving features.
        """
        if self.features is None:
            raise AttributeError('Stock has no features, extractFeatures first')
        return writer.writeFeatures(self)
