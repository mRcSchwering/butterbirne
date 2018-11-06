# This Python file uses the following encoding: utf-8
import xgboost as xgb
import pandas as pd

from finData.parameterGenerator import ParameterGenerator


# TODO erst mal gucken ob scikit ausreicht
# TODO Klasse für Train/Val Trennung
# TODO Klasse für Repeated CrossVal

# TODO richtige Vola Berechnung
# TODO createABT nochmal überarbeiten -> Xtrain, Xtest

# TODO bin:log auc für isUpperQuart durchziehn


workingDir = './experiments/dowJones_histFeatures_10y_fullYears/'
X = pd.read_csv(workingDir + 'X.csv', index_col=0)
Y = pd.read_csv(workingDir + 'Y.csv', index_col=0)

Xtrain = X[:200]
Ytrain = Y[:200]
Xtest = X[200:300]
Ytest = Y[200:300]
dtrain = xgb.DMatrix(Xtrain, label=Ytrain.isUpperQuart)
dtest = xgb.DMatrix(Xtest, label=Ytest.isUpperQuart)


def isModelTooComplex(trainAuc, testAuc):
    if testAuc <= 0:
        return False
    if trainAuc/testAuc > 1.1:
        return True
    return False


paramSet = {
    'eta': .01,
    'eval_metric': 'auc',
    'objective': 'binary:logistic',
    'silent': 1,
    'nthread': 3,
}
numRound = 1000

resultsList = []
paramGen = ParameterGenerator(10)

for params in paramGen:
    paramSet['max_depth'] = params['max_depth']
    paramSet['subsample'] = params['subsample']
    paramSet['colsample_bytree'] = params['colsample_bytree']

    res = xgb.cv(paramSet, dtrain, num_boost_round=numRound, nfold=5, metrics=['auc'])
    bestNumRound = res['test-auc-mean'].idxmax()
    bestRow = res.loc[bestNumRound]

    resultsList.append(pd.DataFrame({
        'max_depth': paramSet['max_depth'],
        'subsample': paramSet['subsample'],
        'colsample_bytree': paramSet['colsample_bytree'],
        'num_boost_round': bestNumRound,
        'test_auc_mean': bestRow['test-auc-mean'],
        'test_auc_std': bestRow['test-auc-std'],
        'train_auc_mean': bestRow['train-auc-mean'],
        'train_auc_std': bestRow['train-auc-std']
    }, index=[paramGen.i]))

    paramGen.isTooComplex = isModelTooComplex(bestRow['train-auc-mean'], bestRow['test-auc-mean'])

results = pd.concat(resultsList, ignore_index=True)
results

0.75/0.7
# idee ranking objectives ausprobieren
# 2 logregs jeweils gegen gut und schlecht
dtrain = xgb.DMatrix(Xtrain, label=Ytrain.isUpperQuart)
dval = xgb.DMatrix(Xval, label=Yval.isUpperQuart)

from finData.parameterGenerator import ParameterGenerator
paramGen = ParameterGenerator()
paramGen.next(1, 1.2)
paramGen.next(1, 1.2)
paramGen.next(1, 1.2)
paramGen.next(1, 1.2)
paramGen.next(1, 1.2)
paramGen.getResults(0, 0)

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
