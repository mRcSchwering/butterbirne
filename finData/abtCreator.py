# This Python file uses the following encoding: utf-8
import pandas as pd


class WindowIterator(object):
    """
    Iterator for sliding a window of size n over an ordered list of elements.
    Returns the ele
    """

    def __init__(self, elements, n):
        self.n = n  # window size
        self.elements = elements  # all elements available, ordered
        self.n_total = len(elements)  # number of elements available
        self.n_steps = self.n_total - self.n + 1  # number of possible steps
        self.step_i = 0  # step index

    def __iter__(self):
        return self

    def __next__(self):
        if self.step_i >= self.n_steps:
            raise StopIteration
        out = self.elements[self.step_i:(self.step_i + self.n)]
        self.step_i += 1
        return out


class AbtCreator(object):
    """
    Create ABT from long time series data.
    """

    def __init__(self, data, isins, windows,
                 getY=lambda i, d: pd.DataFrame(index=i),
                 timepointCol='tp'):
        self._data = data
        self._isins = isins
        self._windows = windows
        self._getY = getY
        self._tp = timepointCol
        self._checkArguments()

    def getABT(self):
        Y = {}
        for w in self._windows:
            y = self._getTargetForWindow(w[-1], self._getY, self._tp)
            x = self._getVarsForWindow(w[:-1], self._getX, self._tp)
        return Y

    def _getTargetForWindow(self, w, getY, tp):
        Y = pd.DataFrame(index=self._isins)
        df = self._data.loc[self._data[tp] == w]
        y = getY(self._isins, df)
        if y.shape[0] is not Y.shape[0]:
            raise AttributeError('getY returns length %d, expected length %d' % (y.shape[0], Y.shape[0]))
        for col in y.columns:
            Y[col] = list(y[col])
        return Y

    def _getVarsForWindow(self, w, getX, tp):
        X = pd.DataFrame(index=self._isins)
        for i in range(len(w)):
            d = len(w) - i  # distance from target
            df = self._data.loc[self._data[tp] == w[i]]
            x = getX(self._isins, df, d)
            if x.shape[0] is not Y.shape[0]:
                raise AttributeError('getX returns length %d, expected length %d' % (x.shape[0], X.shape[0]))
            for col in x.columns:
                X[col] = list(x[col])
        return X

    def _checkArguments(self):
        if not isinstance(self._data, pd.core.frame.DataFrame):
            raise TypeError('data must be DataFrame')
        if self._tp not in self._data.columns:
            raise AttributeError('timepointCol %s is not in data' % self._tp)
        if self._windows.n < 2:
            raise AttributeError('windows iterator has a window size smaller 2')
        if len(self._isins) is not len(set(self._isins)):
            raise AttributeError('There are dublicate isins')
