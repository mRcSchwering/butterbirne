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
            AbtCreator(pd.DataFrame({'a': ['a', 'b']}), [1, 1], [9, 9], self.W)

    def test_noDataFrame(self):
        with self.assertRaises(TypeError):
            AbtCreator({'a': ['a', 'b']}, [1, 2], [9, 9], self.W)

    def test_tpAndDfNotMatching(self):
        with self.assertRaises(AttributeError):
            AbtCreator(pd.DataFrame({'a': ['a', 'b']}), [1, 2], [9], self.W)

    def test_iteratorSizeSmaller2(self):
        W = WindowIterator([1, 2], 1)
        with self.assertRaises(AttributeError):
            AbtCreator(pd.DataFrame({'a': ['a', 'b']}), [1, 2], [9, 9], W)

    def test_allGood(self):
        AbtCreator(pd.DataFrame({'a': ['a', 'b']}), [1, 2], [9, 9], self.W)


class getTargetForWindow(unittest.TestCase):

    def setUp(self):
        self.W = WindowIterator([1, 2, 3], 2)
        df = pd.DataFrame({'a': ['a', 'b', 'c']})
        self.abt = AbtCreator(df, ['x', 'y'], [2, 2, 3], self.W)

    def test_defaultGetY(self):
        res = self.abt._getTargetForWindow(2, lambda i, d: pd.DataFrame(index=i))
        self.assertIsInstance(res, pd.core.frame.DataFrame)
        self.assertTupleEqual((2, 0), res.shape)
        self.assertListEqual(['x', 'y'], list(res.index))

    def test_2targetCols(self):
        def fun(i, d):
            return pd.DataFrame({'a': i, 'b': i})
        res = self.abt._getTargetForWindow(2, fun)
        self.assertIsInstance(res, pd.core.frame.DataFrame)
        self.assertTupleEqual((2, 2), res.shape)
        self.assertListEqual(['x', 'y'], list(res.index))
        self.assertListEqual(['a', 'b'], list(res.columns))
        for col in res.columns:
            self.assertListEqual(['x', 'y'], list(res[col]))

    def test_windowSubsetsToNothing(self):
        res = self.abt._getTargetForWindow(1, lambda i, d: pd.DataFrame(index=i))
        self.assertIsInstance(res, pd.core.frame.DataFrame)
        self.assertTupleEqual((2, 0), res.shape)

    def test_getYhasWrongAmountOfArgs(self):
        with self.assertRaises(TypeError):
            self.abt._getTargetForWindow(2, lambda a: a,)
        with self.assertRaises(TypeError):
            self.abt._getTargetForWindow(2, lambda a, b, c: a)

    def test_windowIsNotScalar(self):
        with self.assertRaises(TypeError):
            self.abt._getTargetForWindow([2], lambda i, d: pd.DataFrame(index=i))

    def test_getYDidntReturnDataFrame(self):
        with self.assertRaises(TypeError):
            self.abt._getTargetForWindow(2, lambda i, d: 'a')

    def test_getYreturnedWrongShapeDataFrame(self):
        with self.assertRaises(AttributeError):
            self.abt._getTargetForWindow(2, lambda i, d: pd.DataFrame({'a': [1]}))


class getVarsForWindow(unittest.TestCase):

    def setUp(self):
        self.W = WindowIterator([1, 2, 3], 2)
        df = pd.DataFrame({'a': ['a', 'b', 'c']})
        self.abt = AbtCreator(df, ['x', 'y'], [2, 2, 3], self.W)

    def test_defaultGetX(self):
        res = self.abt._getVarsForWindow([1, 2], lambda i, d, p: pd.DataFrame(index=i))
        self.assertIsInstance(res, pd.core.frame.DataFrame)
        self.assertTupleEqual((2, 0), res.shape)
        self.assertListEqual(['x', 'y'], list(res.index))

    def test_getXreturnsDuplicateColumns(self):
        with self.assertRaises(AttributeError):
            self.abt._getVarsForWindow([1, 2], lambda i, d, p: pd.DataFrame({'a': i}))

    def test_return1colPerPosition(self):
        res = self.abt._getVarsForWindow([1, 2], lambda i, d, p: pd.DataFrame({p: i}))
        self.assertIsInstance(res, pd.core.frame.DataFrame)
        self.assertTupleEqual((2, 2), res.shape)
        self.assertListEqual(['x', 'y'], list(res.index))
        self.assertListEqual([2, 1], list(res.columns))
        for col in res.columns:
            self.assertListEqual(['x', 'y'], list(res[col]))

    def test_windowSubsetsToNothing(self):
        res = self.abt._getVarsForWindow([4, 5], lambda i, d, p: pd.DataFrame(index=i))
        self.assertIsInstance(res, pd.core.frame.DataFrame)
        self.assertTupleEqual((2, 0), res.shape)

    def test_getXhasWrongAmountOfArgs(self):
        with self.assertRaises(TypeError):
            self.abt._getVarsForWindow([1, 2], lambda a, b: a,)
        with self.assertRaises(TypeError):
            self.abt._getVarsForWindow([1, 2], lambda a, b, c, d: a)

    def test_windowIsScalar(self):
        with self.assertRaises(TypeError):
            self.abt._getVarsForWindow(2, lambda i, d, p: pd.DataFrame(index=i))

    def test_getXdidntReturnDataFrame(self):
        with self.assertRaises(TypeError):
            self.abt._getVarsForWindow([1, 2], lambda i, d, p: 'a')

    def test_getXreturnedWrongShapeDataFrame(self):
        with self.assertRaises(AttributeError):
            self.abt._getVarsForWindow([1, 2], lambda i, d, p: pd.DataFrame({p: [1]}))


class getYtests(unittest.TestCase):

    def concatValues(self, isins, df):
        y = ['%s:%s' % (isin, '_'.join(df['a'])) for isin in isins]
        return pd.DataFrame({'t': y})

    def test_singleTarget(self):
        W = WindowIterator([1, 2, 3], 2)
        df = pd.DataFrame({'a': ['a', 'b', 'c']})
        abt = AbtCreator(df, ['x', 'y'], [2, 2, 3], W)

        res = abt._getTargetForWindow(2, self.concatValues)
        self.assertTupleEqual((2, 1), res.shape)
        self.assertEqual('x:a_b', res.iat[0, 0])
        self.assertEqual('y:a_b', res.iat[1, 0])

        res = abt._getTargetForWindow(3, self.concatValues)
        self.assertTupleEqual((2, 1), res.shape)
        self.assertEqual('x:c', res.iat[0, 0])
        self.assertEqual('y:c', res.iat[1, 0])

    def multipleConcats(self, isins, df):
        y1 = ['%s:%s' % (isin, '_'.join(df['a'])) for isin in isins]
        y2 = ['%s:%s' % (isin, '-'.join(df['b'])) for isin in isins]
        return pd.DataFrame({'t1': y1, 't2': y2})

    def test_multipleTargets(self):
        W = WindowIterator([1, 2, 3], 2)
        df = pd.DataFrame({'a': ['a', 'b', 'c'], 'b': ['d', 'e', 'f']})
        abt = AbtCreator(df, ['x', 'y', 'z'], [2, 2, 2], W)

        res = abt._getTargetForWindow(2, self.multipleConcats)
        self.assertTupleEqual((3, 2), res.shape)
        self.assertEqual('x:a_b_c', res.iat[0, 0])
        self.assertEqual('y:a_b_c', res.iat[1, 0])
        self.assertEqual('z:a_b_c', res.iat[2, 0])
        self.assertEqual('x:d-e-f', res.iat[0, 1])
        self.assertEqual('y:d-e-f', res.iat[1, 1])
        self.assertEqual('z:d-e-f', res.iat[2, 1])

        res = abt._getTargetForWindow(3, self.multipleConcats)
        self.assertTupleEqual((3, 2), res.shape)
        self.assertEqual('x:', res.iat[0, 0])
        self.assertEqual('y:', res.iat[1, 0])
        self.assertEqual('z:', res.iat[2, 0])
        self.assertEqual('x:', res.iat[0, 1])
        self.assertEqual('y:', res.iat[1, 1])
        self.assertEqual('z:', res.iat[2, 1])


class getXtests(unittest.TestCase):

    def concatValues(self, isins, df, dist):
        y = ['%s:%s' % (isin, '_'.join(df['a'])) for isin in isins]
        return pd.DataFrame({('d%d' % dist): y})

    def test_singleTarget(self):
        W = WindowIterator([1, 2, 3], 2)
        df = pd.DataFrame({'a': ['a', 'b', 'c']})
        abt = AbtCreator(df, ['x', 'y'], [2, 2, 3], W)

        res = abt._getVarsForWindow([2, 3], self.concatValues)
        self.assertTupleEqual((2, 2), res.shape)
        self.assertListEqual(['d2', 'd1'], list(res.columns))
        self.assertEqual('x:a_b', res.iat[0, 0])
        self.assertEqual('y:a_b', res.iat[1, 0])
        self.assertEqual('x:c', res.iat[0, 1])
        self.assertEqual('y:c', res.iat[1, 1])

    def multipleConcats(self, isins, df, dist):
        y1 = ['%s:%s' % (isin, '_'.join(df['a'])) for isin in isins]
        y2 = ['%s:%s' % (isin, '-'.join(df['b'])) for isin in isins]
        return pd.DataFrame({('t1_d%d' % dist): y1, ('t2_d%d' % dist): y2})

    def test_multipleTargets(self):
        W = WindowIterator([1, 2, 3], 2)
        df = pd.DataFrame({'a': ['a', 'b', 'c'], 'b': ['d', 'e', 'f']})
        abt = AbtCreator(df, ['x', 'y', 'z'], [2, 2, 2], W)

        res = abt._getVarsForWindow([1, 2], self.multipleConcats)
        self.assertTupleEqual((3, 4), res.shape)
        self.assertListEqual(['t1_d2', 't2_d2', 't1_d1', 't2_d1'], list(res.columns))
        self.assertEqual('x:', res.iat[0, 0])
        self.assertEqual('y:', res.iat[1, 0])
        self.assertEqual('z:', res.iat[2, 0])
        self.assertEqual('x:', res.iat[0, 1])
        self.assertEqual('y:', res.iat[1, 1])
        self.assertEqual('z:', res.iat[2, 1])
        self.assertEqual('x:a_b_c', res.iat[0, 2])
        self.assertEqual('y:a_b_c', res.iat[1, 2])
        self.assertEqual('z:a_b_c', res.iat[2, 2])
        self.assertEqual('x:d-e-f', res.iat[0, 3])
        self.assertEqual('y:d-e-f', res.iat[1, 3])
        self.assertEqual('z:d-e-f', res.iat[2, 3])


class getABTtests(unittest.TestCase):

    def test_withDefaultFunctions(self):
        W = WindowIterator([1, 2, 3, 4], 3)
        df = pd.DataFrame({'A': ['a', 'b', 'c', 'd']})
        abt = AbtCreator(df, ['x', 'y', 'z'], [1, 2, 3, 4], W)
        res = abt.getABT()
        X = res['X']
        Y = res['Y']
        M = res['meta']

        self.assertTupleEqual((6, 1), Y.shape)
        self.assertListEqual(['target'], list(Y.columns))
        self.assertEqual('x:c', Y.iat[0, 0])
        self.assertEqual('y:c', Y.iat[1, 0])
        self.assertEqual('z:c', Y.iat[2, 0])
        self.assertEqual('x:d', Y.iat[3, 0])
        self.assertEqual('y:d', Y.iat[4, 0])
        self.assertEqual('z:d', Y.iat[5, 0])

        self.assertTupleEqual((6, 2), X.shape)
        self.assertListEqual(['feat_d2', 'feat_d1'], list(X.columns))

        self.assertEqual('x:a', X.iat[0, 0])
        self.assertEqual('y:a', X.iat[1, 0])
        self.assertEqual('z:a', X.iat[2, 0])
        self.assertEqual('x:b', X.iat[3, 0])
        self.assertEqual('y:b', X.iat[4, 0])
        self.assertEqual('z:b', X.iat[5, 0])

        self.assertEqual('x:b', X.iat[0, 1])
        self.assertEqual('y:b', X.iat[1, 1])
        self.assertEqual('z:b', X.iat[2, 1])
        self.assertEqual('x:c', X.iat[3, 1])
        self.assertEqual('y:c', X.iat[4, 1])
        self.assertEqual('z:c', X.iat[5, 1])

        self.assertTupleEqual((6, 2), M.shape)
        self.assertListEqual(['window', 'isin'], list(M.columns))
        for i in range(3):
            self.assertEqual(3, M.iat[i, 0])
            self.assertEqual(4, M.iat[i + 3, 0])
        for i in range(2):
            self.assertEqual('x', M.iat[i * 3, 1])
            self.assertEqual('y', M.iat[i * 3 + 1, 1])
            self.assertEqual('z', M.iat[i * 3 + 2, 1])
