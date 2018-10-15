import sys
import pandas as pd

# Data loading
from finData.stock import Stock
from finData.alphavantageDataloader import AlphavantageDataloader

stock = Stock('MSFT', ticker='MSFT')
adapter = AlphavantageDataloader('full')
stock.loadData(adapter)

# calculate features
from finData.statistics import Statistics

prices = stock.data['adj_close']
dailyLogReturns = Statistics.returns(prices.tolist(), log=True)
Statistics.volatilityYearly(dailyLogReturns)
Statistics.performanceYearly(prices)

# TODO obergrenze für vola berechnung
# zZ wird auf kompletten daily returns daily vola berechnet
# aber vllt will ich ne Obergrenze haben, weil zB daily volas von vor
# 20 Jahren nicht mehr aussagekräftig sind
# oder ich kürze vorher das array (also die dailyLogReturns die ich rein gebe)

# TODO garbage collector für nach der feature Berechnung

# TODO Dow Jones Liste

# TODO im Loop mal alles berechnen

# TODO gescheite plotting lib raussuchen

import altair
