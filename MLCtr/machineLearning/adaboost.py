from __future__ import division, print_function
import numpy as np
import math

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
        w = np.full(n_samples, (1 / n_samples))
        self.clfs = []
        # Iterate through classifiers
        for _ in range(self.n_clf):
            clf = DecisionStump()
            min_error = float('inf')

            for feature_i in range(n_features):
                feature_values = np.expand_dims(X[:,feature_i], axis=1)
                unique_values = np.unique(feature_values)

                for threshold in unique_values:
                    p = 1
                    prediction = np.ones(np.shape(y))
                    pre = np.asarray(X[:, feature_i]) <  np.asarray(threshold)
                    prediction[pre] = -1
                    error = np.sum(w[np.asarray(y) !=  np.asarray(prediction)])

                    if error > 0.5:
                        error = 1 - error
                        p = -1

                    if error < min_error:
                        clf.polarity = p
                        clf.threshold = threshold
                        clf.feature_index = feature_i
                        min_error = error

            clf.alpha = 0.5 * np.log((1.0 - min_error) / (min_error + 1e-10))
            predictions = np.ones(np.shape(y))
            negative_idx = (clf.polarity * X[:, clf.feature_index] < clf.polarity * clf.threshold)
            predictions[negative_idx] = -1
            w *= np.exp(-clf.alpha * np.asarray(y) * np.asarray(predictions))
            w /= np.sum(w)

            self.clfs.append(clf)

    def predict(self, X):
        n_samples = np.shape(X)[0]
        y_pred = np.zeros((n_samples, 1))
        for clf in self.clfs:
            # Set all predictions to '1' initially
            predictions = np.ones(np.shape(y_pred))
            # The indexes where the sample values are below threshold
            negative_idx = (clf.polarity * X[:, clf.feature_index] < clf.polarity * clf.threshold)
            # Label those as '-1'
            predictions[negative_idx] = -1
            # Add predictions weighted by the classifiers alpha
            # (alpha indicative of classifier's proficiency)
            y_pred += clf.alpha * predictions
        # Return sign of prediction sum
        y_pred = np.sign(y_pred).flatten()

        return y_pred