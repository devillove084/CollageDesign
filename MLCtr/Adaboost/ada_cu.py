from __future__ import division, print_function

import sys
sys.path.append("..")
sys.path.append(".")

from utils import train_test_split, accuracy_score, Plot

import numpy as np
import cupy
import math
from sklearn import datasets
import matplotlib.pyplot as plt
import pandas as pd

class DecisionStump():
    def __init__(self):
        # Determines if sample shall be classified as -1 or 1 given threshold
        self.polarity = 1
        # The index of the feature used to make classification
        self.feature_index = None
        # The threshold value that the feature should be measured against
        self.threshold = None
        # Value indicative of the classifier's accuracy
        self.alpha = None

class AdaBoost():
    def __init__(self,n_clf=5):
        self.n_clf = n_clf

    def fit(self, X, y):

        n_samples, n_features = np.shape(X)
        # Initialize weights to 1/N
        w = cupy.full(n_samples, (1 / n_samples))
        self.clfs = []
        # Iterate through classifiers
        for _ in range(self.n_clf):
            clf = DecisionStump()
            min_error = float('inf')

            for feature_i in range(n_features):
                feature_values = cupy.expand_dims(X[:,feature_i], axis=1)
                unique_values = cupy.unique(feature_values)

                for threshold in unique_values:
                    p = 1
                    prediction = cupy.ones(np.shape(y))
                    pre = cupy.asarray(X[:, feature_i]) <  cupy.asarray(threshold)
                    prediction[pre] = -1
                    error = cupy.sum(w[cupy.asarray(y) !=  cupy.asarray(prediction)])

                    if error > 0.5:
                        error = 1 - error
                        p = -1

                    if error < min_error:
                        clf.polarity = p
                        clf.threshold = threshold.get()
                        clf.feature_index = feature_i
                        min_error = error

            clf.alpha = 0.5 * cupy.log((1.0 - min_error) / (min_error + 1e-10))
            predictions = cupy.ones(np.shape(y))
            negative_idx = (clf.polarity * X[:, clf.feature_index] < clf.polarity * clf.threshold)
            predictions[negative_idx] = -1
            w *= cupy.exp(-clf.alpha * cupy.asarray(y) * cupy.asarray(predictions))
            w /= cupy.sum(w)

            self.clfs.append(clf)

    def predict(self, X):
        n_samples = np.shape(X)[0]
        y_pred = cupy.zeros((n_samples, 1))
        for clf in self.clfs:
            # Set all predictions to '1' initially
            predictions = cupy.ones(np.shape(y_pred))
            # The indexes where the sample values are below threshold
            negative_idx = (clf.polarity * X[:, clf.feature_index] < clf.polarity * clf.threshold)
            # Label those as '-1'
            predictions[negative_idx] = -1
            # Add predictions weighted by the classifiers alpha
            # (alpha indicative of classifier's proficiency)
            y_pred += clf.alpha * predictions
        # Return sign of prediction sum
        y_pred = cupy.sign(y_pred).flatten()

        return y_pred


def main():
    data = datasets.load_digits()
    X = data.data
    y = data.target

    digit1 = 1
    digit2 = 8
    idx = np.append(np.where(y == digit1)[0], np.where(y == digit2)[0])
    y = data.target[idx]
    # Change labels to {-1, 1}
    y[y == digit1] = -1
    y[y == digit2] = 1
    X = data.data[idx]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)

    # Adaboost classification with 5 weak classifiers
    clf = AdaBoost(n_clf=10)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred.get())
    print ("Accuracy:", accuracy)

if __name__ == "__main__":
    main()
