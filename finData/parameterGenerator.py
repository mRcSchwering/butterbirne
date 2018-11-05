# This Python file uses the following encoding: utf-8
import pandas as pd
import random


class ParameterGenerator(object):
    """
    Do random search for parameters with primitive feature of taking difference
    between train and test metrics into consideration.
    Use next() and getResults()
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

    def __init__(self):
        self.i = 0
        for param in self.parameters:
            self.parameters[param]['value'] = self.parameters[param]['start']
        self._createCaptureLists()

    def next(self, train, test):
        """
        Provide train and test results from previous run
        to get next set of parameters.
        """
        self._capture['iter'].append(self.i)
        self._capture['train'].append(train)
        self._capture['test'].append(test)
        newValues = self._getNewValues(train, test)
        self._updateParameters(newValues)
        self.i += 1
        return newValues

    def getResults(self, train, test):
        """
        Provide train and test results from previous run
        and get summary of parameter sets and results as DataFrame.
        """
        self._capture['iter'].append(self.i)
        self._capture['train'].append(train)
        self._capture['test'].append(test)
        return pd.DataFrame(self._capture)

    def _getNewValues(self, train, test):
        vals = dict()
        isTooComplex = self._modelTooComplex(train, test)
        for param in self.parameters:
            vals[param] = self._getNewValue(param, isTooComplex)
        return vals

    def _getNewValue(self, param, isTooComplex):
        if param == 'max_depth' and isTooComplex:
            preVal = self._capture[param][-1]
            pop = [d for d in self.parameters[param]['range'] if d < preVal]
            if len(pop) < 1:
                return 1
            return random.sample(pop, 1)[0]
        return random.sample(self.parameters[param]['range'], 1)[0]

    def _updateParameters(self, values):
        for param in self.parameters:
            self.parameters[param]['value'] = values[param]
            self._capture[param].append(values[param])

    def _createCaptureLists(self):
        cap = {'iter': [], 'train': [], 'test': []}
        for param in self.parameters:
            cap[param] = [self.parameters[param]['value']]
        self._capture = cap

    @classmethod
    def _modelTooComplex(cls, metricTrain, metricTest):
        if metricTrain <= 0:
            return False
        return True if metricTest/metricTrain > 1.1 else False
