# This Python file uses the following encoding: utf-8
import pandas as pd
import datetime as dt
from procedures.getHistFeatures import getHistFeatures


# Dow Jones as of 10/2018
dowJones = pd.read_csv('data/dowJones.csv')
dowJones.drop(['Date Added', 'Exchange', 'Notes'], axis=1, inplace=True)
dowJones.columns

# add Google, Amazon, facebook
# (which are not in the DowJones, but larger than any DowJones company)
extra = pd.DataFrame({
    'ISIN': ['US02079K3059', 'US02079K1079', 'US30303M1027', 'US0231351067'],
    'Company': ['Alphabet A', 'Alphabet C', 'Facebook', 'Amazon'],
    'Symbol': ['GOOGL', 'GOOG', 'FB', 'AMZN'],
    'Industry': ['Information technologies', 'Information technologies', 'Information technologies', 'Information technologies'],
})
dowJones = dowJones.append(extra)

getHistFeatures(dowJones,
                outfile='data/dowJones_histFeatures_10y.csv',
                latest=dt.date.today(),
                nYears=10)
