# This Python file uses the following encoding: utf-8
import math
import statistics
import datetime


class Statistics(object):

        tradingDaysPerYear = 252
        daysPerYear = 365

        @classmethod
        def returns(cls, prices, log=False):
            """
            Calculate returns from a list of (absolute) prices
            log=True for ln(returns)
            """
            if len(prices) < 2:
                raise AttributeError('There must be at least 2 prices')
            ret = []
            for i in range(1, len(prices)):
                ret.append(prices[i] / prices[i - 1])
            return [math.log(x) for x in ret] if log else ret

        @classmethod
        def volatility(cls, dailyLogReturns, extrapol={'daily': 1}):
            """
            Calculate volatility based on list of daily log returns.
            Extrapolate with dict given (default={'daily': 1})
            As of https://en.wikipedia.org/wiki/Volatility_(finance)
            """
            daily = statistics.stdev(dailyLogReturns)
            volas = {}
            for k, d in extrapol.items():
                volas[k] = daily * math.sqrt(d)
            return volas

        @classmethod
        def volatilityYearly(cls, dailyLogReturns, maxYears=5):
            """
            Calculate volatilities based logged daily returns.
            Extrapolated to YTD, 1 year, years, up to maxYears(default=5)
            """
            dayOfTradingYear = cls.getDayOfTradingYear('today')
            cls._checkListLength(dailyLogReturns, dayOfTradingYear)
            cls._checkListLength(dailyLogReturns, maxYears * cls.tradingDaysPerYear)
            params = {'YTD': dayOfTradingYear}
            for year in range(1, maxYears + 1):
                params['year' + str(year)] = cls.tradingDaysPerYear * year
            return cls.volatility(dailyLogReturns, params)

        @classmethod
        def fuzzyReturns(cls, prices, daysGoingBack, averageOver=15):
            """
            Calculate returns between different time points T1 and T2
            for a list of prices for consecutive trading days.

            T2 is the last list entry in prices.
            T1 is "daysGoingBack" steps from the last list entry.

            Instead of taking 2 single days, the average around T1 and T2 are
            taken with averageOver (default=15).
            Set to 1 for 2 single days.
            """
            ker = round((averageOver - 1) / 2)
            cls._checkListLength(prices, daysGoingBack + ker)
            window = prices[-(daysGoingBack + ker):-(daysGoingBack - ker - 1)]
            t1 = statistics.mean(window)
            t2 = statistics.mean(prices[-(1 + ker):])
            return t2 / t1

        @classmethod
        def performanceYearly(cls, prices, maxYears=5):
            """
            Calculate performance as returns averaged over 15 days for YTD,
            1 year, 2 years, etc. up to 5 years.
            """
            dayOfTradingYear = cls.getDayOfTradingYear('today')
            perf = {'YTD': cls.fuzzyReturns(prices, dayOfTradingYear)}
            for year in range(1, maxYears + 1):
                perf['year' + str(year)] = cls.fuzzyReturns(prices, year * cls.tradingDaysPerYear)
            return perf

        @classmethod
        def getDayOfTradingYear(cls, date='today'):
            """
            Calculate day of trading year from either "today"
            or a given datetime.date.
            """
            if date == 'today':
                date = datetime.date.today()
            if not isinstance(date, datetime.date):
                raise TypeError('date must be "today" or datetime.date')
            dayOfYear = date.timetuple().tm_yday
            return round(cls.tradingDaysPerYear * dayOfYear / cls.daysPerYear)

        @classmethod
        def _checkListLength(cls, x, exp):
            if len(x) < exp:
                raise AttributeError('Need %s values, %s provided' % (exp, len(x)))
