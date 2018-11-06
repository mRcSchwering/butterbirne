# This Python file uses the following encoding: utf-8
import pandas as pd
import random


class ParameterGenerator(object):
    """
    Iterator for generating parameter generator for random search over parameter space.
    Arg     N int maximum number of iterations
    Attr    isTooComplex bool whether previous set of parameters resulted in a too complex model
    """

    parameters = {
        'max_depth': {
            'range': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'start': 6
        },
        'subsample': {
            'range': [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            'start': 0.5
        },
        'colsample_bytree': {
            'range': [0.5, 0.6, 0.7, 0.8, 0.9, 1],
            'start': 0.8
        }
    }

    def __init__(self, N):
        self.i = 0  # current iteration
        self.N = N  # maximum number of iteration
        self.isTooComplex = False  # whether current model is too complex

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.N:
            raise StopIteration
        if self.i < 1:
            self._setStartValues()
        else:
            self._updateParameters(self.isTooComplex)
        self.i += 1
        return self._getParamValues()

    def _getNewValue(self, param, isTooComplex):
        if param == 'max_depth' and isTooComplex:
            preVal = self.parameters[param]['value']
            pop = [d for d in self.parameters[param]['range'] if d < preVal]
            if len(pop) < 1:
                return 1
            return random.sample(pop, 1)[0]
        return random.sample(self.parameters[param]['range'], 1)[0]

    def _updateParameters(self, isTooComplex):
        for param in self.parameters:
            self.parameters[param]['value'] = self._getNewValue(param, isTooComplex)

    def _setStartValues(self):
        for param in self.parameters:
            self.parameters[param]['value'] = self.parameters[param]['start']

    def _getParamValues(self):
        out = dict()
        for param in self.parameters:
            out[param] = self.parameters[param]['value']
        return out
