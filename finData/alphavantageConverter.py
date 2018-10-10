# This Python file uses the following encoding: utf-8
import json
import pandas as pd

from finData.constants import Constants


class AlphavantageConverter(object):

    def __init__(self):
        self._mapping = self._getMapping()

    def responseToDataFrame(self, response):
        """
        Convert AlphavantageApi response to DataFrame with Datetime Index
        """
        data = response['Time Series (Daily)']
        df = self._createDataFrame(data)
        return self._customizeDataFrame(df)

    def _customizeDataFrame(self, df):
        newCols = []
        for col in df.columns:
            hits = [d['to'] for d in self._mapping if d['from'] in col]
            nchars = [len(d) for d in hits]
            newCols.append(hits[nchars.index(max(nchars))])
        df.columns = newCols
        return df.astype('float')

    @classmethod
    def _createDataFrame(cls, data):
        records = []
        dates = []
        for key in data.keys():
            records.append(data[key])
            dates.append(key)
        df = pd.DataFrame.from_records(records, index=pd.DatetimeIndex(dates))
        return df.sort_index()

    @classmethod
    def _getMapping(cls):
        return Constants.columnConversions['alphavantage']
