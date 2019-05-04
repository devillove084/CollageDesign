from __future__ import division
from itertools import combinations_with_replacement
import numpy as np
import cupy
import math
import sys

def judge_type(X):
    if isinstance(X, cupy.ndarray):
        pass
    else:
        X = cupy.asarray(X,dtype=float)
        print(type(X))
    return X

def shuffle_data(X, y, seed=None):
    """ Random shuffle of the samples in X and y """
    judge_type(X)
    judge_type(y)
    if seed:
        cupy.random.seed(seed)
    idx = cupy.arange(X.shape[0])
    cupy.random.shuffle(idx)
    return X[idx.get()], y[idx.get()]


def batch_iterator(X, y=None, batch_size=64):
    """ Simple batch generator """
    judge_type(X)
    n_samples = X.shape[0]
    for i in cupy.arange(0, n_samples, batch_size):
        begin, end = i, min(i+batch_size, n_samples)
        if y is not None:
            yield X[begin:end], y[begin:end]
        else:
            yield X[begin:end]


def divide_on_feature(X, feature_i, threshold):
    """ Divide dataset based on if sample value on feature index is larger than
        the given threshold """
    judge_type(X)
    split_func = None
    if isinstance(threshold, int) or isinstance(threshold, float):
        split_func = lambda sample: sample[feature_i] >= threshold
    else:
        split_func = lambda sample: sample[feature_i] == threshold

    X_1 = cupy.array([sample for sample in X if split_func(sample)],dtype=float)
    X_2 = cupy.array([sample for sample in X if not split_func(sample)],dtype=float)

    #return cupy.array([X_1, X_2,dtype=float)
    return X_1,X_2



def polynomial_features(X, degree):
    judge_type(X)
    n_samples, n_features = cupy.shape(X)

    def index_combinations():
        combs = [combinations_with_replacement(range(n_features), i) for i in range(0, degree + 1)]
        flat_combs = [item for sublist in combs for item in sublist]
        return flat_combs
    
    combinations = index_combinations()
    n_output_features = len(combinations)
    X_new = cupy.empty((n_samples, n_output_features))
    
    for i, index_combs in enumerate(combinations):  
        X_new[:, i] = cupy.prod(X[:, index_combs], axis=1)

    return X_new


def get_random_subsets(X, y, n_subsets, replacements=True):
    """ Return random subsets (with replacements) of the data """
    judge_type(X)
    n_samples = cupy.shape(X)[0]
    # Concatenate x and y and do a random shuffle
    X_y = cupy.concatenate((X, y.reshape((1, len(y))).T), axis=1)
    cupy.random.shuffle(X_y)
    subsets = []

    # Uses 50% of training samples without replacements
    subsample_size = int(n_samples // 2)
    if replacements:
        subsample_size = n_samples      # 100% with replacements

    for _ in range(n_subsets):
        idx = cupy.random.choice(
            range(n_samples),
            size=cupy.shape(range(subsample_size)),
            replace=replacements)
        X = X_y[idx][:, :-1]
        y = X_y[idx][:, -1]
        subsets.append([X, y])
    return subsets


def normalize(X, axis=-1, order=2):
    """ Normalize the dataset X """
    judge_type(X)
    l2 = cupy.atleast_1d(cupy.linalg.norm(X, order, axis))
    l2[l2 == 0] = 1
    return X / cupy.expand_dims(l2, axis)


def standardize(X):
    """ Standardize the dataset X """
    judge_type(X)
    X_std = X
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    for col in range(cupy.shape(X)[1]):
        if std[col]:
            X_std[:, col] = (X_std[:, col] - mean[col]) / std[col]
    # X_std = (X - X.mean(axis=0)) / X.std(axis=0)
    return X_std


def train_test_split(X, y, test_size=0.5, shuffle=True, seed=None):
    """ Split the data into train and test sets """
    judge_type(X)
    if shuffle:
        X, y = shuffle_data(X, y, seed)
    # Split the training data from test data in the ratio specified in
    # test_size
    split_i = len(y) - int(len(y) // (1 / test_size))
    X_train, X_test = X[:split_i], X[split_i:]
    y_train, y_test = y[:split_i], y[split_i:]

    return X_train, X_test, y_train, y_test


def k_fold_cross_validation_sets(X, y, k, shuffle=True):
    """ Split the data into k sets of training / test data """
    judge_type(X)
    if shuffle:
        X, y = shuffle_data(X, y)

    n_samples = len(y)
    left_overs = {}
    n_left_overs = (n_samples % k)
    if n_left_overs != 0:
        left_overs["X"] = X[-n_left_overs:]
        left_overs["y"] = y[-n_left_overs:]
        X = X[:-n_left_overs]
        y = y[:-n_left_overs]

    X_split = np.split(X, k)
    y_split = np.split(y, k)
    sets = []
    for i in range(k):
        X_test, y_test = X_split[i], y_split[i]
        X_train = cupy.concatenate(X_split[:i] + X_split[i + 1:], axis=0)
        y_train = cupy.concatenate(y_split[:i] + y_split[i + 1:], axis=0)
        sets.append([X_train, X_test, y_train, y_test])

    # Add left over samples to last set as training samples
    if n_left_overs != 0:
        np.append(sets[-1][0], left_overs["X"], axis=0)
        np.append(sets[-1][2], left_overs["y"], axis=0)

    return cupy.array(sets)


def to_categorical(x, n_col=None):
    """ One-hot encoding of nominal values """
    if not n_col:
        n_col = cupy.amax(x) + 1
    one_hot = cupy.zeros((x.shape[0], n_col))
    one_hot[cupy.arange(x.shape[0]), x] = 1
    return one_hot


def to_nominal(x):
    """ Conversion from one-hot encoding to nominal """
    return cupy.argmax(x, axis=1)


def make_diagonal(x):
    """ Converts a vector into an diagonal matrix """
    m = cupy.zeros((len(x), len(x)))
    for i in range(len(m[0])):
        m[i, i] = x[i]
    return m
