# This Python file uses the following encoding: utf-8
import unittest
import pandas as pd

from finData.parameterGenerator import ParameterGenerator


class ParameterGeneratorTest(unittest.TestCase):

    def test_modelTooComplex(self):
        res = ParameterGenerator._modelTooComplex(1, 1)
        self.assertFalse(res)
        res = ParameterGenerator._modelTooComplex(1, 1.11)
        self.assertTrue(res)
        res = ParameterGenerator._modelTooComplex(0, 1)
        self.assertFalse(res)
        res = ParameterGenerator._modelTooComplex(1, 0)
        self.assertFalse(res)

    def test_startValueGiven(self):
        ps = ParameterGenerator()
        for param in ps.parameters:
            self.assertEqual(ps.parameters[param]['start'], ps.parameters[param]['value'])

    def test_createCaptureLists(self):
        ps = ParameterGenerator()
        exp = set(['iter', 'train', 'test', 'max_depth', 'subsample', 'colsample_bytree'])
        self.assertSetEqual(exp, set(ps._capture.keys()))
        for param in ['iter', 'train', 'test']:
            self.assertListEqual([], ps._capture[param])
        self.assertListEqual([6], ps._capture['max_depth'])
        self.assertListEqual([0.5], ps._capture['subsample'])
        self.assertListEqual([0.8], ps._capture['colsample_bytree'])

    def test_getNewValueIfTooComplex(self):
        ps = ParameterGenerator()
        self.assertEqual(6, ps._capture['max_depth'][-1])
        for i in range(10):
            self.assertLess(ps._getNewValue('max_depth', True), 6)
            subs = ps._getNewValue('subsample', True)
            self.assertLessEqual(subs, 0.8)
            self.assertGreaterEqual(subs, 0.2)
            cols = ps._getNewValue('colsample_bytree', True)
            self.assertLessEqual(cols, 1)
            self.assertGreaterEqual(cols, 0.5)

    def test_getNewValuesIfTooComplex(self):
        ps = ParameterGenerator()
        self.assertEqual(6, ps._capture['max_depth'][-1])
        for i in range(10):
            res = ps._getNewValues(1, 1.2)
            self.assertLess(res['max_depth'], 6)
            self.assertGreaterEqual(res['max_depth'], 1)
            self.assertLessEqual(res['subsample'], 0.8)
            self.assertGreaterEqual(res['subsample'], 0.2)
            self.assertLessEqual(res['colsample_bytree'], 1)
            self.assertGreaterEqual(res['colsample_bytree'], 0.5)

    def test_next(self):
        ps = ParameterGenerator()
        self.assertEqual(6, ps._capture['max_depth'][-1])
        ps.next(0, 0)
        params = ps.next(1, 1)
        self.assertSetEqual(set(['max_depth', 'subsample', 'colsample_bytree']), set(params.keys()))
        for key in ['iter', 'train', 'test']:
            self.assertEqual(2, len(ps._capture[key]))
            self.assertListEqual([0, 1], ps._capture[key])
        for param in params:
            self.assertEqual(3, len(ps._capture[param]))

    def test_getResults(self):
        ps = ParameterGenerator()
        ps.next(0, 0)
        ps.next(1, 1)
        res = ps.getResults(2, 2)
        self.assertTupleEqual((3, 6), res.shape)
        for key in ['iter', 'train', 'test']:
            self.assertListEqual([0, 1, 2], list(res[key]))
