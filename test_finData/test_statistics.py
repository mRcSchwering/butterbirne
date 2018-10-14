# This Python file uses the following encoding: utf-8
import unittest
import math
import numpy as np
import pandas as pd
import datetime as dt

from finData.statistics import Statistics


class Returns(unittest.TestCase):

    def test_correctReturns(self):
        prices = [1, 2, 1, 1]
        returns = Statistics.returns(prices)
        self.assertEqual(3, len(returns))
        self.assertEqual(2, returns[0])
        self.assertEqual(0.5, returns[1])
        self.assertEqual(1, returns[2])

    def test_correctLogReturns(self):
        prices = [1, 2, 1, 1]
        returns = Statistics.returns(prices, log=True)
        self.assertEqual(3, len(returns))
        self.assertEqual(math.log(2), returns[0])
        self.assertEqual(math.log(0.5), returns[1])
        self.assertEqual(math.log(1), returns[2])

    def test_failIfTooShort(self):
        with self.assertRaises(AttributeError):
            Statistics.returns([1])


class DayOfTradingYear(unittest.TestCase):

    def test_today(self):
        day = Statistics.getDayOfTradingYear()
        self.assertIsInstance(day, int)

    def test_date(self):
        day = Statistics.getDayOfTradingYear(dt.date(2000, 1, 20))
        self.assertIsInstance(day, int)
        self.assertEqual(14, day)


class Volatility(unittest.TestCase):

    def test_correctVolatilities(self):
        x = [-0.5, 0.5, 1, 0]
        volas = Statistics.volatility(x)
        self.assertEqual(['daily'], list(volas.keys()))
        self.assertAlmostEqual(0.645, volas['daily'], places=3)

    def test_correctExtrapolation(self):
        x = [-0.5, 0.5, 1, 0]
        volas = Statistics.volatility(x, {'a': 3})
        self.assertEqual(['a'], list(volas.keys()))
        self.assertAlmostEqual(0.645 * math.sqrt(3), volas['a'], places=2)


class VolatilityYearly(unittest.TestCase):

    def test_correctVolatilities(self):
        x = np.random.normal(100, 1, size=252)
        volas = Statistics.volatilityYearly(x, maxYears=1)
        self.assertSetEqual(set(['YTD', 'year1']), set(volas.keys()))
        self.assertGreaterEqual(volas['year1'], volas['YTD'])
        self.assertGreaterEqual(volas['year1'], 14)
        self.assertLessEqual(volas['year1'], 18)

    def test_tooFewData(self):
        x = np.random.normal(100, 1, size=251)
        with self.assertRaises(AttributeError):
            Statistics.volatilityYearly(x, maxYears=1)

    def test_2years(self):
        def test_correctVolatilities(self):
            x = np.random.normal(100, 1, size=252 * 2)
            volas = Statistics.volatilityYearly(x, maxYears=2)
            self.assertSetEqual(set(['YTD', 'year1']), set(volas.keys()))
            self.assertGreaterEqual(volas['year1'], volas['YTD'])
            self.assertGreaterEqual(volas['year2'], volas['year1'])
            self.assertGreaterEqual(volas['year1'], 14)
            self.assertLessEqual(volas['year1'], 18)
            self.assertAlmostEqual(volas['year1'] * math.sqrt(252), volas['year2'])


class FuzzyReturns(unittest.TestCase):

    def test_correctReturns(self):
        x = [1, 0, 0, 0, 1]
        ret = Statistics.fuzzyReturns(x, 5, 1)
        self.assertEqual(1, ret)

    def test_averageOver3(self):
        x = [3, 4, 2, 0, 2, 4]
        ret = Statistics.fuzzyReturns(x, 5, 3)
        self.assertEqual(1, ret)

    def test_averageOver5(self):
        x = [3, 4, 2, 2, 4, 0, 2, 4, 3]
        ret = Statistics.fuzzyReturns(x, 7, 5)
        self.assertEqual(1, ret)

    def test_tooFewData(self):
        x = [4, 2, 2, 4, 0, 2, 4, 3]
        with self.assertRaises(AttributeError):
            Statistics.fuzzyReturns(x, 7, 5)


class PerformanceYearly(unittest.TestCase):

    def test_correctPerformance(self):
        x = np.random.normal(100, 1, size=259)
        perfs = Statistics.performanceYearly(x, 1)
        self.assertSetEqual(set(['YTD', 'year1']), set(perfs.keys()))
        self.assertGreaterEqual(perfs['YTD'], 0.99)
        self.assertLessEqual(perfs['YTD'], 1.1)
        self.assertGreaterEqual(perfs['year1'], 0.99)
        self.assertLessEqual(perfs['year1'], 1.1)

    def test_tooFewData(self):
        x = np.random.normal(100, 1, size=258)
        with self.assertRaises(AttributeError):
            Statistics.performanceYearly(x, 1)
