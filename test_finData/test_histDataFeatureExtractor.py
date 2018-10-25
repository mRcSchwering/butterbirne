# This Python file uses the following encoding: utf-8
import unittest
from finData.histDataFeatureExtractor import MonthlySteps


class monthlyStepsIterator(unittest.TestCase):

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
