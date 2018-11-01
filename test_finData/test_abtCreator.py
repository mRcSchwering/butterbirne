# This Python file uses the following encoding: utf-8
import unittest
import pandas as pd

from finData.abtCreator import WindowIterator
from finData.abtCreator import AbtCreator


class WindowIteratorTests(unittest.TestCase):

    def test_iterateOverElements(self):
        eles = [1, 2, 3, 4, 5]
        it = WindowIterator(eles, 2)
        windows = list(it)
        self.assertEqual(4, len(windows))
        for window in windows:
            self.assertEqual(2, len(window))
        self.assertListEqual([1, 2], windows[0])

    def test_windowSmallerThanElements(self):
        eles = [1, 2, 3]
        it = WindowIterator(eles, 4)
        windows = list(it)
        self.assertEqual(0, len(windows))

    def test_windowEqualsElements(self):
        eles = [1, 2, 3]
        it = WindowIterator(eles, 3)
        windows = list(it)
        self.assertEqual(1, len(windows))
        self.assertListEqual(eles, windows[0])


class abtCreatorChecks(unittest.TestCase):

    def setUp(self):
        self.W = WindowIterator([1, 2], 2)

    def test_dublicateIsins(self):
        with self.assertRaises(AttributeError):
            AbtCreator(pd.DataFrame({'tp': [1, 2]}), [1, 1], self.W)

    def test_noDataFrame(self):
        with self.assertRaises(TypeError):
            AbtCreator({'tp': [1, 2]}, [1, 2], self.W)

    def test_tpColNotInDf(self):
        with self.assertRaises(AttributeError):
            AbtCreator(pd.DataFrame({'a': [1, 2]}), [1, 1], self.W)

    def test_iteratorSizeSmaller2(self):
        W = WindowIterator([1, 2], 1)
        with self.assertRaises(AttributeError):
            AbtCreator(pd.DataFrame({'tp': [1, 2]}), [1, 1], W)


class getTargetForWindow(unittest.TestCase):

    def setUp(self):
        self.W = WindowIterator([1, 2], 2)
        self.abt = AbtCreator(pd.DataFrame({'tp': [1, 2]}), ['a', 'b'], self.W)

    def test_defaultGetY(self):
        res = self.abt._getTargetForWindow(
            1, lambda i, d: pd.DataFrame(index=i), 'tp')
        self.assertIsInstance(res, pd.core.frame.DataFrame)
        self.assertTupleEqual((2, 0), res.shape)
        self.assertListEqual(['a', 'b'], list(res.index))

    def test_2targetCols(self):
        def fun(i, d):
            return pd.DataFrame({'a': i, 'b': i})
        res = self.abt._getTargetForWindow(1, fun, 'tp')
        self.assertIsInstance(res, pd.core.frame.DataFrame)
        self.assertTupleEqual((2, 2), res.shape)
        self.assertListEqual(['a', 'b'], list(res.index))
        self.assertListEqual(['a', 'b'], list(res.columns))
        for col in res.columns:
            self.assertListEqual(['a', 'b'], list(res[col]))

    def test_windowSubsetsToNothing(self):
        res = self.abt._getTargetForWindow(
            3, lambda i, d: pd.DataFrame(index=i), 'tp')
        self.assertIsInstance(res, pd.core.frame.DataFrame)
        self.assertTupleEqual((2, 0), res.shape)

    def test_getYhasWrongAmountOfArgs(self):
        with self.assertRaises(TypeError):
            self.abt._getTargetForWindow(3, lambda a: a, 'tp', 'trgt')
        with self.assertRaises(TypeError):
            self.abt._getTargetForWindow(3, lambda a, b, c: a, 'tp', 'trgt')

    def test_windowIsNotScalar(self):
        abt = AbtCreator(pd.DataFrame({'tp': [1, 2, 3]}), ['a', 'b'], self.W)
        with self.assertRaises(TypeError):
            abt._getTargetForWindow(
                [5, 6], lambda i, d: pd.DataFrame(index=i), 'tp')

    def test_getYDidntReturnDataFrame(self):
        with self.assertRaises(AttributeError):
            self.abt._getTargetForWindow(1, lambda i, d: 'a', 'tp')

    def test_getYreturnedWrongShapeDataFrame(self):
        with self.assertRaises(AttributeError):
            self.abt._getTargetForWindow(
                1, lambda i, d: pd.DataFrame({'a': [1]}), 'tp')
