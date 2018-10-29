# This Python file uses the following encoding: utf-8
import pandas as pd


class Utils(object):

    @classmethod
    def filterBy(cls, df, month, year):
        """
        Filter df as DataFrame by month and year as integers.
        Returns filtered df sorted by ascending index.
        """
        df = df.loc[[d.month == month and d.year == year for d in df.index]]
        return df.sort_index()

    @classmethod
    def checkStockInfo(cls, df, cols):
        if not isinstance(df, pd.core.frame.DataFrame):
            raise TypeError('df must be a pandas DataFrame')
        if not isinstance(cols, list):
            raise TypeError('cols must be a list')
        for exp in cols:
            if exp not in df.columns:
                raise AttributeError('DataFrame must have a %s column' % exp)
        df = df.astype(str)
        if df.isnull().values.any() or (df.values == '').any():
            raise ValueError('Empty values in DataFrame')
