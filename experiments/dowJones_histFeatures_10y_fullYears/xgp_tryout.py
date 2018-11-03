# This Python file uses the following encoding: utf-8
import xgboost as xgb
import pandas as pd

df = pd.DataFrame({'a': ['a', 'b', 'c']})
isins = ['x', 'y']
tps = [2, 2, 3]
w = 2


isins = ['a', 'b', 'c']
w = 'd1'
['x', 'y'] * 3


l = []
'-'.join(df.iloc[:,0])

l.append(df)
l.append(df)
pd.concat(l, ignore_index=True)



from finData.abtCreator import WindowIterator

# TODO Klasse(n) für X, Y Berechnung pro window, Feature Berechnung möglichst flexibel
# TODO Klasse für Window shifting
# TODO Klasse die alle windows zu einer großen X und Y zusammen baut
# -> ABT als csv oder vllt als DMatrix direkt
# erst mal für diesen use case
# -> refaktorisieren, gucken ob es für fundamental wiederverwendbar wäre

# TODO Klasse für Train/Val Trennung
# TODO Klasse für Repeated CrossVal

# TODO richtige Vola Berechnung

workingDir = './experiments/dowJones_histFeatures_10y_fullYears/'
data = pd.read_csv(workingDir + 'postDQR_long.csv')
isins = list(set(data['isin']))

data['steps'] = data['year'].map(str) + '-' + data['month'].map(str)
stepCol = 'steps'

steps = []
for year in sorted(set(data['year'])):
    for month in sorted(set(data['month'])):
        steps.append(str(year) + '-' + str(month))

windows = WindowIterator(steps, 3)

df = pd.DataFrame({'a': [1, 2, 3], 'b': [1, 2, 3]})
df['c'] = df['a'] + df['b']
df


# Klasse braucht
# isins
# data
ISINS = isins
DATA = data
Y_ = getTargetForWindow(w_y, calculateY)


def calculateY(isins, df):
    y = []
    for isin in isins:
        cond = (df['isin'] == isin) & (df['variable'] == 'logReturn')
        y.append(sum(df.loc[cond]['value']))
    quants = pd.np.quantile(y, [0.25, 0.75])
    return [int(d > quants[1]) for d in y]

abtc = ABTcreator(data, isins, windows, calculateY)

Y = abtc.calculateABT()
Y.keys()
df = pd.DataFrame({'tp': [1, 2]})
df['a'] = 'a'


type(data)
data.loc[data['month'] == [1, 2]]


def a(a):
    return a

class ABTcreator(object):

    def __init__(self, data, isins, windows, getY):
        self._data = data
        self._isins = isins
        self._windows = windows
        self._getY = getY

    def calculateABT(self):
        Y = {}
        for w in self._windows:
            w_y = w[len(w) - 1]
            y = self._getTargetForWindow(w_y, self._getY)
            Y[w_y] = y
        return Y

    def _getTargetForWindow(self, w, getY, step='steps', target='target'):
        Y = pd.DataFrame(index=self._isins)
        df = self._data.loc[self._data[step] == w]
        Y[target] = getY(self._isins, df)
        return Y


[1,2,3][:-1]






T = set([d for d in data['year']])  # all steps available
W = [2014, 2015, 2016]  # window used: last position is predicted
n = len(T)  # number of steps available
m = len(W)  # window size: position in W = distance to prediction position
n - m + 1  # possible time intervals

# calculate features for window
X = pd.DataFrame(index=isins)
for step in range(m - 1):
    p = m - 1 - step
    df = data.loc[data['year'] == W[step]]

    x1 = []
    x2 = []
    for isin in isins:
        cond1 = (df['isin'] == isin) & (df['variable'] == 'logReturn')
        cond2 = (data['isin'] == isin) & (data['variable'] == 'logVola')
        x1.append(sum(df.loc[cond1]['value']))
        x2.append(sum(data.loc[cond2]['value']))
    X['sumLogReturn' + str(p)] = x1
    X['sumLogVola' + str(p)] = x2




# idee ranking objectives ausprobieren
# 2 logregs jeweils gegen gut und schlecht
dtrain = xgb.DMatrix(X, label=Y)

param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic'}
param['nthread'] = 3
param['eval_metric'] = 'auc'

# gibt hier nochmal test an, reicht auch nur train?
evallist = [(dtest, 'eval'), (dtrain, 'train')]

num_round = 10
bst = xgb.train(param, dtrain, num_round)
# mit evallist (4. arg) kann ich dann auch early_stopping_rounds=x eintragen
# eval metric wird für early stopping verwendet


dtest = xgb.DMatrix(X)
ypred = bst.predict(dtest)

fig = xgb.plot_importance(bst).figure
fig.set_size_inches(12, 8)
fig

fig = xgb.plot_tree(bst, num_trees=2).figure
fig.set_size_inches(12, 8)
fig
