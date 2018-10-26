# This Python file uses the following encoding: utf-8
from finData.statistics import Statistics
from finData.utils import Utils
import datetime as dt
import pandas as pd


class MonthlySteps(object):

    def __init__(self, startMonth, startYear, maxYears):
        if maxYears < 1:
            raise AttributeError('maxYears must be > 0')
        self._current = (startMonth, startYear)
        self._startMonth = startMonth
        self._minYear = startYear - maxYears
        self._stopNext = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._stopNext is True:
            raise StopIteration
        self._current = (self._current[0] - 1, self._current[1])
        if self._current[0] < 1:
            self._current = (12, self._current[1] - 1)
        if self._current[1] <= self._minYear and self._current[0] == self._startMonth:
            self._stopNext = True
        return self._current


class HistDataFeatureExtractor(object):
    """
    Adapter for calculating features based on historic stock data.
    Stock needs to have data already loaded.
    Latest is the latest/youngest date from which to start calculating back
    into the past extracting features month by month until maxYears is reached.
    """

    tradingDaysPerMonth = 21

    def __init__(self, latest, maxYears=10):
        if not isinstance(latest, dt.date):
            raise TypeError('latest must be datetime.date')
        self._steps = MonthlySteps(latest.month, latest.year, maxYears)

    def getFeatures(self, stock):
        records = []
        for step in self._steps:
            month = step[0]
            year = step[1]
            df = Utils.filterBy(stock.data, month=month, year=year)
            if df.shape[0] < 3:
                break
            res = self._featuresFromPrices(df['adj_close'].tolist())
            records.append({
                'logReturn': res[0],
                'vola': res[1],
                'month': month,
                'year': year
            })
        return pd.DataFrame.from_records(records)

    @classmethod
    def _featuresFromPrices(cls, prices):
        logReturns = Statistics.returns(prices, log=True)
        monthlyLogReturn = sum(logReturns)
        vola = Statistics.volatility(logReturns, {
            'month': cls.tradingDaysPerMonth
        })
        return (monthlyLogReturn, vola['month'])
