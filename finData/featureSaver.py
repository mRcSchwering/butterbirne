# This Python file uses the following encoding: utf-8
import pandas as pd
import os.path


class FeatureSaver(object):
    """
    Adapter for saving features as csv to outfile.
    Stock needs to have features already extracted.
    If file exists features are appended according to the columns
    that are already existing in the file.
    """

    def __init__(self, outfile):
        self._outfile = outfile

    def writeFeatures(self, stock):
        long = self._makeLong(stock.features)
        out = self._addIsin(long, stock.isin)
        self._writeOutfile(out, self._outfile)

    @classmethod
    def _writeOutfile(cls, df, outfile):
        exists = os.path.isfile(outfile)
        if exists:
            tmp = pd.read_csv(outfile, nrows=1)
            orgCols = tmp.columns.tolist()
            cls._compareSets(orgCols, df.columns.tolist())
            df = df[orgCols]
        with open(outfile, 'a') as ouf:
            df.to_csv(ouf, header=(not exists), index=False)

    @classmethod
    def _addIsin(cls, df, isin):
        df['isin'] = isin
        return df

    @classmethod
    def _makeLong(cls, df):
        return pd.melt(df, id_vars=['year', 'month'])

    @classmethod
    def _compareSets(cls, set1, set2):
        for d in set1:
            if d not in set2:
                raise AttributeError('Existing file has columns %s; DataFrame has columns: %s' % (set1, set2))
