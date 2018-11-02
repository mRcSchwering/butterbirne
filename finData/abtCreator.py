# This Python file uses the following encoding: utf-8
import pandas as pd


class WindowIterator(object):
    """
    Iterator for sliding a window of size n over an ordered list of elements.
    Returns window as list of elements.
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
    Create ABT from long time-series data.

    data: DataFrame
    isins: list of unique ISINs
    timepoints: list of the time point for each row in data
    windows: WindowIterator creating sliding window over time points
    """

    def __init__(self, data, isins, timepoints, windows):
        self._data = data
        self._isins = isins
        self._tps = timepoints
        self._windows = windows
        self._checkArguments()

    def getABT(self, getY=None, getX=None):
        """
        Creates ABT by chronologically moving a time interval as provided by windows.
        For each time interval target and feature variables can be calculated by
        defining getY and getX respectively.
        The resulting ABT is returned as dict of DataFrames for X and Y.
        To make getY, getY work see example methods and their docstrings.
        """
        if getY is None:
            getY = self.getY
        if getX is None:
            getX = self.getX
        y = []
        x = []
        for w in self._windows:
            y.append(self._getTargetForWindow(w[-1], getY))
            x.append(self._getVarsForWindow(w[:-1], getX))
        Y = pd.concat(y, ignore_index=True)
        X = pd.concat(x, ignore_index=True)
        return {'X': X, 'Y': Y}

    def _getTargetForWindow(self, w, getY):
        if isinstance(w, (list, tuple, set, dict)):
            raise TypeError('window for target is not scalar')
        Y = pd.DataFrame(index=self._isins)
        df = self._data.loc[[tp == w for tp in self._tps]]
        y = getY(self._isins, df)
        self._checkFunResults('Y', Y, y)
        for col in y.columns:
            Y[col] = list(y[col])
        return Y

    def _getVarsForWindow(self, w, getX):
        X = pd.DataFrame(index=self._isins)
        for i in range(len(w)):
            d = len(w) - i  # distance from target
            df = self._data.loc[[tp == w[i] for tp in self._tps]]
            x = getX(self._isins, df, d)
            self._checkFunResults('X', X, x)
            for col in x.columns:
                X[col] = list(x[col])
        return X

    def _checkArguments(self):
        if not isinstance(self._data, pd.core.frame.DataFrame):
            raise TypeError('data must be DataFrame')
        if len(self._tps) != self._data.shape[0]:
            raise AttributeError('timepoints has length %d, expected length %d' % (len(self._tps), self._data.shape[0]))
        if self._windows.n < 2:
            raise AttributeError('windows iterator has a window size smaller 2')
        if len(self._isins) is not len(set(self._isins)):
            raise AttributeError('There are duplicate isins')

    @classmethod
    def _checkFunResults(cls, type, mainDf, df):
        if not isinstance(df, pd.core.frame.DataFrame):
            raise TypeError('get%s does not return DataFrame' % type)
        if df.shape[0] != mainDf.shape[0]:
            raise AttributeError('get%s returned %d rows, expected %d rows' % (type, df.shape[0], mainDf.shape[0]))
        dups = [col for col in df.columns if col in mainDf.columns]
        if len(dups) > 0:
            raise AttributeError('get%s returns already existing columns %s' % (type, dups))

    @classmethod
    def getY(self, isins, df):
        """
        This is an example for getY.
        Provide custom getY to getABT for deriving target variable(s).

        must take 2 arguments and return a DataFrame:
        Args    isins: list of unique ISINs
                df: DataFrame of data subsetted to current time point
        Return  DataFrame with as many rows as isins containing target variable(s)

        In every time window, the last time point is to be predicted.
        So, data will be subsetted to the last time point in each window before
        it is handed to getY as df. Use getY to derive target variable(s)
        and return them as DataFrame with 1 row for each ISIN.
        In this example, the data point of each time window are concatnated
        by '-' for each ISIN.
        """
        y = ['%s:%s' % (isin, '-'.join(df.iloc[:, 0])) for isin in isins]
        return pd.DataFrame({'target': y})

    @classmethod
    def getX(self, isins, df, dist):
        """
        This is an example for getX.
        Provide custom getX to getABT for deriving feature variable(s).

        must take 3 arguments and return a DataFrame:
        Args    isins: list of unique ISINs
                df: DataFrame of data subsetted to current time point
                dist: int for distance to target in number of time points
        Return  DataFrame with as many rows as isins containing feature variable(s)

        In every time window, all time points except for the last one are used
        to calculate features for predicting the target variable.
        In every window these time points are iterated over chronologically.
        Data is subset to to contain only values for that time point and then
        handed over to getX as df. Use getX to derive feature variable(s)
        and return them as DataFrame with 1 row for each ISIN.
        In this example, the data points of each time point are concatnated
        by '-' for each ISIN.
        Since there can be more than 1 time point per window, the column name
        for the derived feature is altered with dist. This is the distance in
        time points to the last column (the target column).
        """
        y = ['%s:%s' % (isin, '-'.join(df.iloc[:, 0])) for isin in isins]
        return pd.DataFrame({('feat_d%s' % dist): y})
