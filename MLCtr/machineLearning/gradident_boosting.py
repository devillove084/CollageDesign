from __future__ import division, print_function
import numpy as np
import progressbar
import cupy


from graduateutil import train_test_split, standardize, to_categorical, judge_type
from graduateutil import mean_squared_error, accuracy_score
from graduateutil.loss_functions import SquareLoss, CrossEntropy
from graduateutil.misc import bar_widgets
from .decision_tree import RegressionTree


class GradientBoosting(object):
    """Super class of GradientBoostingClassifier and GradientBoostinRegressor. 
    Uses a collection of regression trees that trains on predicting the gradient
    of the loss function. 

    Parameters:
    -----------
    n_estimators: int
        The number of classification trees that are used.
    learning_rate: float
        The step length that will be taken when following the negative gradient during
        training.
    min_samples_split: int
        The minimum number of samples needed to make a split when building a tree.
    min_impurity: float
        The minimum impurity required to split the tree further. 
    max_depth: int
        The maximum depth of a tree.
    regression: boolean
        True or false depending on if we're doing regression or classification.
    """
    def __init__(self, n_estimators, learning_rate, min_samples_split,
                 min_impurity, max_depth, regression):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.min_samples_split = min_samples_split
        self.min_impurity = min_impurity
        self.max_depth = max_depth
        self.regression = regression
        self.bar = progressbar.ProgressBar(widgets=bar_widgets)

        # Square loss for regression
        # Log loss for classification
        self.loss = SquareLoss()
        if not self.regression:
            self.loss = CrossEntropy()
        
        # Initialize regression trees
        self.trees = []
        for _ in range(n_estimators):
            tree = RegressionTree(
                    min_samples_split=self.min_samples_split,
                    min_impurity=min_impurity,
                    max_depth=self.max_depth)
            self.trees.append(tree)


    def fit(self, X, y):
        judge_type(X)
        judge_type(y)

        y_pred = cupy.full(y.shape, cupy.mean(y, axis=0))
        
        print(type(y_pred))
        for i in self.bar(range(self.n_estimators)):
            gradient = self.loss.gradient(y, y_pred)
            self.trees[i].fit(X, gradient)
            update = self.trees[i].predict(X)
            # Update y prediction

            y_pred -= cupy.multiply(self.learning_rate, update)


    def predict(self, X):
        judge_type(X)
        y_pred = cupy.array([])
        # Make predictions
        for tree in self.trees:
            update = tree.predict(X)
            update = cupy.multiply(self.learning_rate, update)
            y_pred = -update if not y_pred.any() else y_pred - update

        if not self.regression:
            # Turn into probability distribution
            y_pred = cupy.exp(y_pred) / cupy.expand_dims(cupy.sum(cupy.exp(y_pred), axis=1), axis=1)
            # Set label to the value that maximizes probability
            y_pred = cupy.argmax(y_pred, axis=1)
        return y_pred
    

class GradientBoostingRegressor(GradientBoosting):
    def __init__(self, n_estimators=20, learning_rate=0.5, min_samples_split=2,
                 min_var_red=1e-7, max_depth=4, debug=False):
        super(GradientBoostingRegressor, self).__init__(n_estimators=n_estimators,
            learning_rate=learning_rate,
            min_samples_split=min_samples_split,
            min_impurity=min_var_red,
            max_depth=max_depth,
            regression=True)

class GradientBoostingClassifier(GradientBoosting):
    def __init__(self, n_estimators=200, learning_rate=.5, min_samples_split=2,
                 min_info_gain=1e-7, max_depth=2, debug=False):
        super(GradientBoostingClassifier, self).__init__(n_estimators=n_estimators,
            learning_rate=learning_rate,
            min_samples_split=min_samples_split,
            min_impurity=min_info_gain,
            max_depth=max_depth,
            regression=False)

    def fit(self, X, y):
        y = to_categorical(y)
        super(GradientBoostingClassifier, self).fit(X, y)
