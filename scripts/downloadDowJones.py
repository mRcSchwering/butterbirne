# This Python file uses the following encoding: utf-8
import pandas as pd
import datetime as dt
from procedures.getCurrentRiskPerformanceData import getCurrentRiskPerformanceData


# Dow Jones as of 10/2018
dowJones = pd.read_csv('data/dowJones.csv')
dowJones.drop(['Date Added', 'Exchange', 'Notes'], axis=1, inplace=True)


# add Google, Amazon, facebook
# (which are not in the DowJones, but larger than any DowJones company)
extra = pd.DataFrame({
    'Company': ['Alphabet A', 'Alphabet C', 'Facebook', 'Amazon'],
    'Symbol': ['GOOGL', 'GOOG', 'FB', 'AMZN'],
    'Industry': ['Information technologies', 'Information technologies', 'Information technologies', 'Information technologies'],
})
dowJones = dowJones.append(extra)


today = dt.date.today()
getCurrentRiskPerformanceData(dowJones, 'data/riskPerformance_dowJones_5years_%s.pkl' % str(today))
