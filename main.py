import pandas as pd


from finData.stock import Stock
from finData.alphavantageDataloader import AlphavantageDataloader


stock = Stock('MSFT', ticker='MSFT')
adapter = AlphavantageDataloader('compact')

stock.loadData(adapter)
stock.data


from finData.statistics import Statistics


df = stock.histData # ist ascending

prices = df['adj_close']
logReturns = Statistics.returns(prices.tolist(), log=True)
volas = Statistics.volatility(logReturns)
perf = Statistics.performance(prices, fuzzy=30)
perf


# TODO tests for Statistics
# for 'small' only calculate possible values

# TODO wie mit loadData + adapter für features
# -> flexibles anhängen von features wie mit data

# TODO cleanup methode für data
