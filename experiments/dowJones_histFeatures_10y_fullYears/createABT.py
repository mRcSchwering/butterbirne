# This Python file uses the following encoding: utf-8
import pandas as pd
from finData.abtCreator import WindowIterator
from finData.abtCreator import AbtCreator

workingDir = './experiments/dowJones_histFeatures_10y_fullYears/'
data = pd.read_csv(workingDir + 'postDQR_long.csv')

isins = list(set(data['isin']))
tps = list(data['year'].map(str) + '-' + data['month'].map(str))

timeline = []
for year in sorted(set(data['year'])):
    for month in sorted(set(data['month'])):
        timeline.append(str(year) + '-' + str(month))
len(timeline) is 9 * 12


def getY(isins, df):
    y = []
    for isin in isins:
        c = (df['isin'] == isin) & (df['variable'] == 'logReturn')
        logRet = df.loc[list(c)]['value']
        if logRet.shape[0] != 1:
            raise ValueError('getY error got logReturn length %d' % logRet.shape[0])
        y.append(logRet.iat[0])
    quants = pd.np.quantile(y, [0.25, 0.75])
    Y = pd.DataFrame({
        'target_logReturn': y,
        'isUpperQuart': [int(d > quants[1]) for d in y],
        'isLowerQuart': [int(d < quants[0]) for d in y]
    })
    return Y


def getX(isins, df, dist):
    rets = []
    vols = []
    for isin in isins:
        cond1 = (df['isin'] == isin) & (df['variable'] == 'logReturn')
        cond2 = (df['isin'] == isin) & (df['variable'] == 'logVola')
        logRet = df.loc[list(cond1)]['value']
        logVol = df.loc[list(cond2)]['value']
        if logRet.shape[0] != 1:
            raise ValueError('getX error got logReturn length %d' % logRet.shape[0])
        if logVol.shape[0] != 1:
            raise ValueError('getX error got logReturn length %d' % logVol.shape[0])
        rets.append(logRet.iat[0])
        vols.append(logVol.iat[0])
    X = pd.DataFrame({
        ('logReturn_d%d' % dist): rets,
        ('logVola_d%d' % dist): vols
    })
    return X


windows = WindowIterator(timeline, 3)
abt = AbtCreator(data, isins, tps, windows)
res = abt.getABT(getY, getX)

Y = res['Y']
X = res['X']
X['logReturnSum'] = X['logReturn_d2'] + X['logReturn_d1']
X['logVolaSum'] = X['logVola_d2'] + X['logVola_d1']
X['logReturnDelta'] = X['logReturn_d2'] - X['logReturn_d1']
X['logVolaDelta'] = X['logVola_d2'] - X['logVola_d1']

Y.to_csv(workingDir + 'Y.csv')
X.to_csv(workingDir + 'X.csv')
