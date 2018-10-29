# This Python file uses the following encoding: utf-8
import pandas as pd
import datetime as dt
import time

from finData.utils import Utils
from finData.stock import Stock
from finData.alphavantageDataloader import AlphavantageDataloader
from finData.histDataFeatureExtractor import HistDataFeatureExtractor
from finData.featureSaver import FeatureSaver


def getHistFeatures(stockInfoDf, outfile, latest, nYears=10):
    """
    Download historic prices, then calculate volatilities and performances
    for the past nYears for the DataFrame of stocks provided.
    Save the results as csv.

    stockInfoDf is the DataFrame with stock information.
    It must have column 'Symbol' with the ticker and column 'Company' with
    the name. Can have more info though.
    """
    Utils.checkStockInfo(stockInfoDf, cols=['Symbol', 'ISIN', 'Company'])
    downloader = AlphavantageDataloader('full')
    extractor = HistDataFeatureExtractor(latest, maxYears=nYears)
    saver = FeatureSaver(outfile)

    print('Starting downloads...\n')
    for i in range(len(stockInfoDf.index)):

        row = stockInfoDf.iloc[i]
        stock = Stock(isin=row['ISIN'], name=row['Company'], ticker=row['Symbol'])
        print('%s (%s)' % (stock.name, stock.isin))

        stock.loadData(downloader)
        print('\tdata for %d trading days' % stock.data.shape[0])
        stock.extractFeatures(extractor)
        print('\t%d features extracted' % stock.features.shape[0])
        stock.saveFeatures(saver)
        time.sleep(20)

    print('\n...done')
