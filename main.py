import pandas as pd


from finData.stock import Stock
from finData.statistics import Statistics


stock = Stock('MSFT', outputsize='small')
df = stock.histData # ist ascending

prices = df['adj_close']
logReturns = Statistics.returns(prices.tolist(), log=True)
volas = Statistics.volatility(logReturns)
perf = Statistics.performance(prices, fuzzy=30)
perf


# TODO tests for Statistics
# for 'small' only calculate possible values
# everything should end up on stock object
# discard raw data?
# garbage collector?
