# This Python file uses the following encoding: utf-8
import pandas as pd
import time

from finData.stock import Stock
from finData.alphavantageDataloader import AlphavantageDataloader
from finData.statistics import Statistics


def getCurrentRiskPerformanceData(stockInfoDf,
                                  outfile,
                                  nYears=5):
    """
    Download historic prices, then calculate volatilities and performances
    for the past nYears for the DataFrame of stocks provided.
    Save the results as csv.

    stockInfoDf is the DataFrame with stock information.
    It must have column 'Symbol' with the ticker and column 'Company' with
    the name. Can have more info though.
    """
    nTradingDaysPerYear = 252
    fuzzyReturns = 15
    nDays = nTradingDaysPerYear * nYears + round(fuzzyReturns / 2)

    # check integrity
    if not isinstance(stockInfoDf, pd.core.frame.DataFrame):
        raise TypeError('stockInfoDf must be a pandas DataFrame')
    for exp in ['Symbol', 'Company']:
        if exp not in stockInfoDf.columns:
            raise AttributeError('stockInfoDf must have a %d column' % exp)
    stockInfoDf = stockInfoDf.astype(str)
    if stockInfoDf.isnull().values.any():
        raise ValueError('Empty values in stockInfoDf')

    # collector
    features = pd.DataFrame({
        'Symbol': [],
        'Timeperiod': [],
        'Volatility': [],
        'Performance': []
    })

    print('Starting downloads...\n')
    adapter = AlphavantageDataloader('full')

    # for each stock
    for i in range(len(stockInfoDf.index)):

        # prepare stock
        row = stockInfoDf.iloc[i]
        stock = Stock(isin=row['Company'], ticker=row['Symbol'])
        print(stock.name)

        # load data
        stock.loadData(adapter)
        stock.data = stock.data[-nDays:]

        # in case of to little data, continue
        if len(stock.data.index) < nDays:
            print('!!!Warning: To little data: %s rows!!!' % len(stock.data.index))
            del stock
            continue

        # calculate features
        prices = stock.data['adj_close']
        dailyLogReturns = Statistics.returns(prices.tolist(), log=True)
        volas = Statistics.volatilityYearly(dailyLogReturns, maxYears=nYears)
        perfs = Statistics.performanceYearly(prices)

        # check all features were calculated
        if not set(perfs.keys()) == set(volas.keys()):
            print('\t!!!Warning: Keys of performances and volatilities dont match!!!')
            del stock, prices, dailyLogReturns
            continue

        # combine into 1 dataframe
        keys = list(volas.keys())
        df = pd.DataFrame({
            'Symbol': [stock.ticker] * len(keys),
            'Timeperiod': keys,
            'Volatility': [volas[tp] for tp in keys],
            'Performance': [perfs[tp] for tp in keys]
        })

        # assure types
        df[['Symbol', 'Timeperiod']] = df[['Symbol', 'Timeperiod']].astype(str)
        df[['Volatility', 'Performance']] = df[['Volatility', 'Performance']].astype(float)

        # append to collector
        features = features.append(df)

        # clean up
        del stock, prices, dailyLogReturns

        # wait for alphavantage call volume barrier
        time.sleep(20)

    print('...done with downloading\nmerging and saving...')

    # merge with stockInfoDf
    merged = stockInfoDf.set_index('Symbol').join(features.set_index('Symbol'))

    # save
    merged.to_csv(outfile)
    print('...done')
