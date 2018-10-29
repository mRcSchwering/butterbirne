# This Python file uses the following encoding: utf-8
import unittest
import statistics
import pandas as pd
import datetime as dt
from finData.histDataFeatureExtractor import MonthlySteps, HistDataFeatureExtractor


class MockStock(object):

    def __init__(self):
        self.data = pd.read_pickle('testdata/histData_MMM.pkl')


class MonthlyStepsIterator(unittest.TestCase):

    def test_startingOneMonthInPast(self):
        a = MonthlySteps(3, 2010, 1)
        self.assertEqual(2, a.__next__()[0])

    def test_finishesWithStartingMonth(self):
        a = MonthlySteps(3, 2010, 1)
        self.assertEqual(3, list(a)[-1][0])

    def test_goesThroughMonths(self):
        a = MonthlySteps(2, 2010, 1)
        self.assertEqual([1, 12, 11], [d[0] for d in list(a)[:3]])

    def test_expectedLength(self):
        a = MonthlySteps(2, 2010, 2)
        self.assertEqual(2 * 12, len(list(a)))

    def test_startMonth1doesntScrewUp(self):
        a = MonthlySteps(1, 2010, 1)
        self.assertEqual(12, len(list(a)))

    def test_assureMaxYearsAbove0(self):
        with self.assertRaises(AttributeError):
            MonthlySteps(1, 1000, 0)


class FeaturesFromPrices(unittest.TestCase):

    def test_lessThan3valuesFails(self):
        HistDataFeatureExtractor._featuresFromPrices([1, 2, 3])
        with self.assertRaises(statistics.StatisticsError):
            HistDataFeatureExtractor._featuresFromPrices([1, 2])

    def test_someDefinitionResults(self):
        res = HistDataFeatureExtractor._featuresFromPrices([1, 1, 1])
        self.assertTupleEqual((0, 0), res)
        res = HistDataFeatureExtractor._featuresFromPrices([1, 2, 1])
        self.assertEqual(0, res[0])
        self.assertAlmostEqual(4.49, res[1], places=2)
        res = HistDataFeatureExtractor._featuresFromPrices([2, 1, 2])
        self.assertEqual(0, res[0])
        self.assertAlmostEqual(4.49, res[1], places=2)
        res = HistDataFeatureExtractor._featuresFromPrices([1, 0.00001, 1])
        self.assertEqual(0, res[0])
        self.assertLess(4.49, res[1])

    def test_failsForUnexpectedValues(self):
        with self.assertRaises(ValueError):
            HistDataFeatureExtractor._featuresFromPrices([1, 1, 0])
        with self.assertRaises(ValueError):
            HistDataFeatureExtractor._featuresFromPrices([1, 1, -1])


class getFeatures(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s = MockStock()

    def test_noDateGiven(self):
        with self.assertRaises(TypeError):
            HistDataFeatureExtractor(1)

    def test_cannotReachMaxYears(self):
        h = HistDataFeatureExtractor(dt.date(2018, 10, 10))
        res = h.getFeatures(self.s)
        self.assertTupleEqual((4, 4), res.shape)
        exp = ['month', 'year', 'logReturn', 'vola']
        self.assertSetEqual(set(exp), set(res.columns))
        self.assertSetEqual(set([2018]), set(res['year'].tolist()))
        self.assertListEqual([9, 8, 7, 6], res['month'].tolist())

    def test_latestDateIsTooLate(self):
        h = HistDataFeatureExtractor(dt.date(2018, 12, 1))
        res = h.getFeatures(self.s)
        self.assertTupleEqual((0, 0), res.shape)

    def test_latestDateIsTooEarly(self):
        h = HistDataFeatureExtractor(dt.date(2017, 1, 1))
        res = h.getFeatures(self.s)
        self.assertTupleEqual((0, 0), res.shape)

    def test_iteratorIsReloadedOnEveryCall(self):
        h = HistDataFeatureExtractor(dt.date(2018, 10, 10))
        res = h.getFeatures(self.s)
        self.assertTupleEqual((4, 4), res.shape)
        res = h.getFeatures(self.s)
        self.assertTupleEqual((4, 4), res.shape)
