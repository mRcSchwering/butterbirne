# This Python file uses the following encoding: utf-8
import xgboost as xgb
import pandas as pd

# TODO Klasse für hyperparameter tuning

# TODO Klasse für Train/Val Trennung
# TODO Klasse für Repeated CrossVal

# TODO richtige Vola Berechnung

workingDir = './experiments/dowJones_histFeatures_10y_fullYears/'
X = pd.read_csv(workingDir + 'X.csv', index_col=0)
Y = pd.read_csv(workingDir + 'Y.csv', index_col=0)

Xtrain = X[:200]
Ytrain = Y[:200]
Xval = X[200:300]
Yval = Y[200:300]
Xtest = X[300:400]
Ytest = Y[300:400]


# idee ranking objectives ausprobieren
# 2 logregs jeweils gegen gut und schlecht
dtrain = xgb.DMatrix(Xtrain, label=Ytrain.isUpperQuart)
dval = xgb.DMatrix(Xval, label=Yval.isUpperQuart)

param = {
    'max_depth': 7,
    'gamma': .3,
    'eta': .01,
    'silent': 1,
    'objective': 'binary:logistic',
    'subsample': 1,
    'colsample_bytree': 1,
    'alpha': 0,
}
param['nthread'] = 3
param['eval_metric'] = 'auc'

# gibt hier nochmal test an, reicht auch nur train?
evallist = [(dval, 'eval'), (dtrain, 'train')]

num_round = 10000
bst = xgb.train(param, dtrain, num_round, evallist, early_stopping_rounds=100)

# cv mit eval:auc scheint nicht zu gehen
# man kann aber eigene FUnktion für eval definieren:
#https://github.com/dmlc/xgboost/issues/1226
# das scheint dann zu gehen (gibt feval, maximize)
bst = xgb.cv(param, dtrain, num_boost_round=num_round, nfold=5, metrics=['auc'])
# mit evallist (4. arg) kann ich dann auch early_stopping_rounds=x eintragen
# eval metric wird für early stopping verwendet
# mit verbose_eval=False hält der die fresse
# mal eval_metrics angucken



dtest = xgb.DMatrix(Xtest)
ypred = bst.predict(dtest)
sum(ypred[list(Ytest.isUpperQuart == 1)] > 0.1) / sum(list(Ytest.isUpperQuart == 1))

bst.attributes()
bst.attr('best_iteration')
dir(bst)
3*3*5*20 * 10 /60/60


xgb.plot_importance(bst).figure.set_size_inches(12, 8)

xgb.plot_tree(bst, num_trees=2).figure.set_size_inches(12, 8)
