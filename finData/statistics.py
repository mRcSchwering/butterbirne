# This Python file uses the following encoding: utf-8
import math
import statistics
import datetime


class Statistics(object):

        tradingDays = 252
        normalDays = 365

        @classmethod
        def returns(cls, prices, log=False):
            """
            Calculate returns from a list of (absolute) prices
            log=True for ln(returns)
            """
            ret = []
            for i in range(1, len(prices)):
                ret.append(prices[i] / prices[i - 1])
            return [math.log(x) for x in ret] if log else ret

        @classmethod
        def volatility(cls, dailyLogReturns):
            """
            Calculate volatilities based logged daily returns.
            Extrapolated to monthly, yearly, and several years.
            As of https://en.wikipedia.org/wiki/Volatility_(finance)
            """
            daily = statistics.stdev(dailyLogReturns)
            volas = {
                'daily': daily,
                'monthly': daily * math.sqrt(cls.tradingDays / 12),
                'yearly': daily * math.sqrt(cls.tradingDays),
                '3year': daily * math.sqrt(cls.tradingDays * 3),
                '5year': daily * math.sqrt(cls.tradingDays * 5)
            }
            return volas

        @classmethod
        def performance(cls, prices, fuzzy=10):
            """
            Calculate returns between different time points.
            Fuzzy gives the number of days over which to take the mean
            when getting the price for a time point.
            fuzzy=1 for taking exact days
            """
            def getT1(x, m, s):
                return statistics.mean(x[-(m + s):-(m - s)])
            t2 = statistics.mean(prices[-(fuzzy * 2):])
            dayOfYear = datetime.date.today().timetuple().tm_yday
            dayOfTradingYear = cls.tradingDays * dayOfYear / cls.normalDays
            perf = {
                'YTD': t2 / getT1(prices, round(dayOfTradingYear), fuzzy),
                '1year': t2 / getT1(prices, cls.tradingDays, fuzzy),
                '3year': t2 / getT1(prices, cls.tradingDays * 2, fuzzy),
                '5year': t2 / getT1(prices, cls.tradingDays * 5, fuzzy)
            }
            return perf
