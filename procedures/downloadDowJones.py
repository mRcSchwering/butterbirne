# This Python file uses the following encoding: utf-8
import pandas as pd
import time

from finData.stock import Stock
from finData.alphavantageDataloader import AlphavantageDataloader
from finData.statistics import Statistics


# Dow Jones as of 10/2018
dowJones = pd.read_csv('data/dowJones.csv')
dowJones.drop(['Date Added', 'Exchange', 'Notes'], axis=1, inplace=True)

# add Google, Amazon, facebook
# (which are not in the DowJones, but larger than any DowJones company)
extra = pd.DataFrame({
    'Company': ['Alphabet A', 'Alphabet C', 'Facebook', 'Amazon'],
    'Symbol': ['GOOGL', 'GOOG', 'FB', 'AMZN'],
    'Industry': ['Information technologies', 'Information technologies', 'Information technologies', 'Information technologies'],
})
dowJones = dowJones.append(extra)

# check integrity
dowJones = dowJones.astype(str)
if dowJones.isnull().values.any():
    raise ValueError('Empty values in DataFrame')


# choosing how far to go back for volatility calculation
# a bit fore than 5 years in trading days
nDays = 1300
adapter = AlphavantageDataloader('full')

# collector
features = pd.DataFrame({
    'Symbol': [],
    'Timeperiod': [],
    'Volatility': [],
    'Performance': []
})


# for each stock
for i in range(len(dowJones.index)):

    # prepare stock
    row = dowJones.iloc[i]
    stock = Stock(isin=row['Company'], ticker=row['Symbol'])
    print(stock.name)

    # load data
    stock.loadData(adapter)
    stock.data = stock.data[-nDays:]

    # in case of to little data, continue
    if len(stock.data.index) < nDays:
        print('To little data: %s rows' % len(stock.data.index))
        del stock
        continue

    # calculate features
    prices = stock.data['adj_close']
    dailyLogReturns = Statistics.returns(prices.tolist(), log=True)
    volas = Statistics.volatilityYearly(dailyLogReturns)
    perfs = Statistics.performanceYearly(prices)

    # check all features were calculated
    if not set(perfs.keys()) == set(volas.keys()):
        print('Keys of performances and volatilities dont match')
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


# merge with dowJones
merged = dowJones.set_index('Symbol').join(features.set_index('Symbol'))

# save
merged.to_pickle('data/dowJones.pkl')
