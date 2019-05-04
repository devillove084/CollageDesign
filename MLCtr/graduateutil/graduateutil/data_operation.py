from __future__ import division
import numpy as np
import math
import sys
import cupy

def judge_type(X):
    if isinstance(X, cupy.ndarray):
        pass
    else:
        X = cupy.asarray(X,dtype=float)

def calculate_entropy(y):
    """ Calculate the entropy of label array y """
    judge_type(y)
    log2 = lambda x: cupy.log(x) / cupy.log(2)
    unique_labels = cupy.unique(y)
    entropy = 0
    for label in unique_labels:
        count = len(y[y == label])
        p = count / len(y)
        entropy += -p * log2(p)
    return entropy


def mean_squared_error(y_true, y_pred):
    """ Returns the mean squared error between y_true and y_pred """
    judge_type(y_true)
    judge_type(y_pred)
    mse = cupy.mean(cupy.power(y_true - y_pred, 2))
    return mse


def calculate_variance(X):
    """ Return the variance of the features in dataset X """
    #X_ = cupy.asarray(X,dtype=float)
    judge_type(X)
    mean = cupy.ones(X.shape) * X.mean(0)
    n_samples = X.shape[0]
    variance = (1 / n_samples) * cupy.diag((X - mean).T.dot(X - mean))
    
    return variance


def calculate_std_dev(X):
    """ Calculate the standard deviations of the features in dataset X """
    judge_type(X)
    std_dev = cupy.sqrt(calculate_variance(X))
    return std_dev


def euclidean_distance(x1, x2):
    """ Calculates the l2 distance between two vectors """
    judge_type(x1)
    judge_type(x2)
    distance = 0
    # Squared distance between each coordinate
    for i in range(x1.__len__):
        distance += pow((x1[i] - x2[i]), 2)
    return cupy.sqrt(distance)


def accuracy_score(y_true, y_pred):
    """ Compare y_true to y_pred and return the accuracy """
    judge_type(y_true)
    judge_type(y_pred)
    accuracy = cupy.sum(y_true == y_pred, axis=0) / y_true.__len__
    return accuracy


def calculate_covariance_matrix(X, Y=None):
    """ Calculate the covariance matrix for the dataset X """
    if Y is None:
        Y = X
    n_samples = np.shape(X)[0]
    covariance_matrix = (1 / (n_samples-1)) * (X - X.mean(axis=0)).T.dot(Y - Y.mean(axis=0))

    return np.array(covariance_matrix, dtype=float)
 

def calculate_correlation_matrix(X, Y=None):
    """ Calculate the correlation matrix for the dataset X """
    if Y is None:
        Y = X
    n_samples = np.shape(X)[0]
    covariance = (1 / n_samples) * (X - X.mean(0)).T.dot(Y - Y.mean(0))
    std_dev_X = np.expand_dims(calculate_std_dev(X), 1)
    std_dev_y = np.expand_dims(calculate_std_dev(Y), 1)
    correlation_matrix = np.divide(covariance, std_dev_X.dot(std_dev_y.T))

    return np.array(correlation_matrix, dtype=float)
