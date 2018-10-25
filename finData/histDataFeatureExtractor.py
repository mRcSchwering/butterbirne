# This Python file uses the following encoding: utf-8
from finData.statistics import Statistics
from finData.utils import Utils
import datetime as dt


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
    Adapter for downloading historic prices for stock.
    Stock needs to have correct "ticker" attribute.
    Outputsize can be 'compact' for the last 100 entries
    or 'full' (default) for all data.
    """

    def __init__(self, latest, maxYears=10):
        if not isinstance(latest, dt.date):
            raise TypeError('latest must be datetime.date')
        self._steps = MonthlySteps(latest.month, latest.year, maxYears)

    def getFeatures(self, stock):
        records = []

        for step in steps:
            month = step[0]
            year = step[1]
            df = Utils.filterBy(stock.data, month=month, year=year)

            if df.shape[0] < 3:
                break

            prices = df['adj_close'].tolist()
            logReturns = Statistics.returns(prices, log=True)
            monthlyLogReturn = sum(logReturns)
            vola = Statistics.volatility(logReturns, {'month': 21})

            records.append({
                'year': year,
                'month': month,
                'logReturn': monthlyLogReturn,
                'vola': vola
            })
            # TODO testen
        return records
