from sklearn.cross_validation import cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix, roc_curve
from sklearn.grid_search import RandomizedSearchCV
from sklearn.metrics import roc_curve, precision_score, recall_score
from scipy.stats import randint as sp_randint
import numpy as np

class ModelParams(object):
    """
    Create an object of the model, its parameters, name etc...
    Instance Attributes:
        self.model: sklearn model
        self.params: set of parameters for grid search
        self.name: name of the model (string)
    List of methods:
    __init__: class initialization
    """
    def __init__(self, model, params, name):
        """
        Initialization of the class adding its most important attributes.
        Args:
            model: sklearn model
            params: set of parameters for grid search
            name: name of the model (string)
        """
        self.model = model
        self.params = params
        self.name = name

class ModelComparator(object):
    """
    Compare models and store score information in the model objects.
    Instance Attributes:
        self.model_scoring: method used for the scoring of the model
        self.models_params: list of ModelParams objects
        self.X: exogenous variable
        self.y: endogenous variable
        self.X_train: exogenous train variable
        self.y_train: endogenous train variable
        self.X_test: exogenous test variable
        self.y_test: endogenous test variable
    List of methods:
    __init__: instance initialization
    compare_models: calculate score values and roc for each model
    best_model: find the best estimator for a specific model
    cross_val: calculate the cross validation scores
    test: calculate the score for the test
    model_roc_curve: calculate roc curve values
    """
    def __init__(self, models_params, X, y, scoring):
        """
        Initialization fo the instance
        Args:
            models_params: list of ModelParams objects
            X: exogenous variable
            y: endogenous variable
            scoring: method for scoring
        """
        self.model_scoring = scoring
        self.models_params = models_params
        self.X = X
        self.y = y
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y, test_size=0.3,
            random_state=0)

    def compare_models(self):
        """
        Iterate through each model and calculate most important scores and
        parameters for roc curve
        """
        for model in self.models_params:
            model.best_estimator = self.best_model(model)
            model.cross_val = self.cross_val(model)
            model.test_score = self.test(model)
            model.fpr, model.tpr, model.threshold = self.model_roc_curve(model)

    def best_model(self, model, iter=20):
        """
        Find the best model using a random search of the parameters.
        Args:
            model: estimator used for the random parameters search
            iter: number of iteration of the random search
        Return:
            best_estimator: Best estimator found
        """
        rndGrid = RandomizedSearchCV(model.model,
            model.params, n_iter=iter, scoring=self.model_scoring, n_jobs=-1)
        rndGrid.fit(self.X_train, self.y_train)
        best_estimator = rndGrid.best_estimator_
        return best_estimator

    def cross_val(self, model):
        """
        Cross validate the model using a 5 folds cross validation
        Args:
            model: ModelParams object used for the cross validation
        Return:
            score: score of the cross validation
        """
        score = cross_val_score(estimator=model.best_estimator, X=self.X_train,\
        y = self.y_train, scoring=self.model_scoring, cv=5, n_jobs=-1)
        return score

    def test(self, model):
        """
        Assess score on the test set
        Args:
            model: ModelParams object
        Return:
            score: score of the test validation

        """
        model.best_estimator.fit(self.X_train, self.y_train)
        y_pred = model.best_estimator.predict(self.X_test)
        if self.model_scoring == 'recall':
            score = recall_score(self.y_test, y_pred)
        elif self.model_scoring == 'precision':
            score = precision_score(self.y_test, y_pred)
        return score

    def model_roc_curve(self, model):
        """
        Produce information for plotting the roc curve

        """
        model.model.fit(self.X_train, self.y_train)
        prob = model.model.predict_proba(self.X_test)
        fpr, tpr, threshold = roc_curve(self.y_test.values, prob, pos_label=1)
        return fpr, tpr, threshold
