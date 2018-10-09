# encoding: utf-8
import pandas as pd

from finData.alphavantageApi import AlphavantagApi
api = AlphavantagApi()

params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'MSFT',
    'outputsize': 'full'  # 'compact' for 100 latest
}
res = api.request(params)


res.keys()
res.get('Meta Data')
df = res.get('Time Series (Daily)')
min(df.keys())


# TODO sowas wie stock klasse, wo ich zB hist data dran hängen kann
# -> einfacher mehrere stocks im loop zu laden

# TODO column conversions in constants
# TODO sowas wie url auch in constants

# TODO sowas hier in utils klasse
@classmethod
    def _reshape(cls, df, mapping):
        """
        Convert DataFrame using a mapping

        Mapping is list of dicts with each 'from' and 'to'.
        DataFrame columns are renamed 'from', 'to'.

        Names not appearing in mapping are not included in dataframe.
        """
        old_colnames = [c['from'] for c in mapping]
        df = df[old_colnames]
        new_colnames = []
        for old in old_colnames:
            new = [c['to'] for c in mapping if c['from'] == old]
            new_colnames.append(new[0])
        df.columns = new_colnames
        return df

    @classmethod
    def getColumnConversions(cls, filename):
        with open(filename) as inf:
            obj = json.load(inf)
        return obj
