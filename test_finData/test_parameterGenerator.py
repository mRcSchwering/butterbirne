# This Python file uses the following encoding: utf-8
import unittest
import pandas as pd

from finData.parameterGenerator import ParameterGenerator


class ParameterGeneratorTest(unittest.TestCase):

    def test_constructor(self):
        paramGen = ParameterGenerator(10)
        self.assertFalse(paramGen.isTooComplex)
        self.assertEqual(10, paramGen.N)
        self.assertEqual(0, paramGen.i)

    def test_startValuesSet(self):
        paramGen = ParameterGenerator(10)
        params = paramGen.__next__()
        self.assertEqual(6, params['max_depth'])
        self.assertEqual(0.5, params['subsample'])
        self.assertEqual(0.8, params['colsample_bytree'])

    def test_iterateSomeValues(self):
        paramGen = ParameterGenerator(10)
        for params in paramGen:
            self.assertGreaterEqual(params['max_depth'], 1)
            self.assertLessEqual(params['max_depth'], 9)
            self.assertGreaterEqual(params['subsample'], 0.2)
            self.assertLessEqual(params['subsample'], 0.8)
            self.assertGreaterEqual(params['colsample_bytree'], 0.5)
            self.assertLessEqual(params['colsample_bytree'], 1)

    def test_modelIsGettingTooComplex(self):
        paramGen = ParameterGenerator(20)
        prevDepth = 6
        for params in paramGen:
            self.assertLessEqual(params['max_depth'], prevDepth)
            prevDepth = params['max_depth']
            paramGen.isTooComplex = True

    def test_reliableNumberOfIterations(self):
        i = 0
        paramGen = ParameterGenerator(20)
        for params in paramGen:
            i += 1
        self.assertEqual(20, i)
