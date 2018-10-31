# This Python file uses the following encoding: utf-8
import xgboost as xgb
import pandas as pd

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

# calculate labels for window
Y = pd.DataFrame(index=isins)
df = data.loc[data['year'] == W[m - 1]]
y = []
for isin in isins:
    cond1 = (df['isin'] == isin) & (df['variable'] == 'logReturn')
    y.append(sum(df.loc[cond1]['value']))

quants = pd.np.quantile(y, [0.25, 0.75])
Y['label'] = [int(d > quants[1]) for d in y]



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
