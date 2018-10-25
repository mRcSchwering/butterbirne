# This Python file uses the following encoding: utf-8


class Utils(object):

    @classmethod
    def filterBy(cls, df, month, year):
        """
        Filter df as DataFrame by month and year as integers.
        Returns filtered df sorted by ascending index.
        """
        df = df.loc[[d.month == month and d.year == year for d in df.index]]
        return df.sort_index()
