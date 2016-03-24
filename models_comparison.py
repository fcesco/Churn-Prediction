from sklearn import cross_validation
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklarn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix, roc_curve
from sklearn.metrics import confusion_matrix roc_curve
from sklearn.grid_search import RandomizedSearchCV
from scipy.stats import randint as sp_randint
import numpy as np


class model_params(object):
    def __init__(self, model, params):
        self.model
        self.params


class ModelComparator(object):
    def __init__(self, models_params, X, y):
        self.models_params = models_params
        self.X = X
        self.y = y
        self.X_train, self.X_test, self.y_train, self.y_test = \
            cross_validation.train_test_split(X, y, test_size=0.3,
            random_state=0)


    def train_model(self):
        for model in self.models:
            model_param.model.fit(self.X_train, self.y_train)


    def best_model(self, iter=20):
        for model in self.models:
            rndGrid = RandomizedSearchCV(model_param.model,
                params, n_iter=n_iter)
            rndGrid.fit(X_train, y_train)
            return rndGrid.best_estimator_, rndGrid.best_params


if __name__=="__main__":
    decisionTreeParams = {"max_depth": [9,7,5,3, None],
                          "max_features": sp_randint(1, 11),
                          "min_samples_split": sp_randint(1, 11),
                          "min_samples_leaf": sp_randint(1, 11),
                          "max_leaf_nodes" = [1,2,3,4,5,6,7,8, None]}

    randomForestParams = {"max_depth": [9,7,5,3, None],
                          "max_features": sp_randint(1, 11),
                          "min_samples_split": sp_randint(1, 11),
                          "min_samples_leaf": sp_randint(1, 11),
                          "bootstrap": [True, False],
                          "criterion": ["gini", "entropy"]}

    SDGparams = {"loss" : ['hinge', 'log', 'modified_huber','squared_hinge'],
                        "penalty" : ['l2', 'l1', 'elasticnet'],
                         "alpha": list(np.arange(0.000001, 10, 0.00001))}

    GradBoostparams = {"loss": ['deviance', 'exponential'],
                            "learning_rate": list(np.arange(0.01, 10, 0.8)),
                            "n_estimators": range(10, 100, 10),
                            "max_depth": range(1, 10, 1)
                            "min_samples_split": [2, 4, 6]
                            "min_samples_leaf": [1, 2, 4, 5]}

    tree_param = model_params(DecisionTreeClassifier(), decisionTreeParams)
    rndF_param = model_params(RandomForestClassifier(), randomForestParams)
    sdg_param = model_params(SGDClassifier(), SDGparams)
    grd_param = model_params(GradientBoostingClassifier(), GradBoostClass)
    models = [tree_param, rndF_param, sdg_param, grd_param]
    mod_comp = ModelComparator(models, X, y)
