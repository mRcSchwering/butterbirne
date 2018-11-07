import xgboost as xgb
import pandas as pd
from finData.parameterGenerator import ParameterGenerator
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import roc_auc_score

# TODO custom metric
# TODO early stopping und geringeres learning

# TODO für die anderen strategien
# TODO refactorn


# define hyperparameter search
def parameterSearch(params, dtrain, N):

    numRound = 1000

    def isModelTooComplex(trainAuc, testAuc):
        if testAuc <= 0:
            return False
        if trainAuc/testAuc > 1.1:
            return True
        return False

    resultsList = []
    paramGen = ParameterGenerator(N)

    for paramSet in paramGen:
        params['max_depth'] = paramSet['max_depth']
        params['subsample'] = paramSet['subsample']
        params['colsample_bytree'] = paramSet['colsample_bytree']

        res = xgb.cv(params, dtrain, num_boost_round=numRound,
                     nfold=5, metrics=['auc'])
        bestNumRound = res['test-auc-mean'].idxmax()
        bestRow = res.loc[bestNumRound]

        resultsList.append(pd.DataFrame({
            'max_depth': params['max_depth'],
            'subsample': params['subsample'],
            'colsample_bytree': params['colsample_bytree'],
            'num_boost_round': bestNumRound,
            'test_auc_mean': bestRow['test-auc-mean']
        }, index=[paramGen.i]))

        paramGen.isTooComplex = isModelTooComplex(bestRow['train-auc-mean'], bestRow['test-auc-mean'])

    return pd.concat(resultsList, ignore_index=True)


# define model selection procedure
def modelSelection(params, N, dtrain, dval=None):
    results = parameterSearch(params, dtrain, N)

    bestParams = results.loc[results['test_auc_mean'].idxmax()]
    params['max_depth'] = int(bestParams['max_depth'])
    params['subsample'] = bestParams['subsample']
    params['colsample_bytree'] = bestParams['colsample_bytree']

    model = xgb.train(params, dtrain, int(bestParams['num_boost_round']))

    if dval is None:
        return model

    probs = model.predict(dval)
    y = [int(d) for d in dval.get_label()]
    return roc_auc_score(y, probs)


# load data
workingDir = './experiments/dowJones_histFeatures_10y_fullYears/'

X = pd.read_csv(workingDir + 'Xtrain.csv', index_col=0)
Y = pd.read_csv(workingDir + 'Ytrain.csv', index_col=0)
y = Y.isUpperQuart


# fixed parameters
N = 20
fixedParams = {
    'eta': .01,
    'eval_metric': 'auc',
    'objective': 'binary:logistic',
    'silent': 1,
    'nthread': 3,
}


# get actual model
dtrain = xgb.DMatrix(X, label=y)
model = modelSelection(fixedParams, N, dtrain)

# evaluate model
aucs = []
CV = RepeatedStratifiedKFold(n_splits=3, n_repeats=5)

i = 0
for trainIdx, valIdx in CV.split(X, y):
    i += 1
    print('Round:', i)
    dtrain = xgb.DMatrix(X.iloc[trainIdx], label=y.iloc[trainIdx])
    dval = xgb.DMatrix(X.iloc[valIdx], label=y.iloc[valIdx])
    auc = modelSelection(fixedParams, N, dtrain, dval)
    aucs.append(auc)

aucs

# model
xgb.plot_importance(model).figure.set_size_inches(12, 8)

xgb.plot_tree(model, num_trees=2).figure.set_size_inches(12, 8)
