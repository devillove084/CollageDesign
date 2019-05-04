from __future__ import division
import numpy as np
import cupy

from .data_operation import accuracy_score
from .data_manipulation import judge_type
from .activation_functions import Sigmoid

class Loss(object):
    def loss(self, y_true, y_pred):
        return NotImplementedError()

    def gradient(self, y, y_pred):
        raise NotImplementedError()

    def acc(self, y, y_pred):
        return 0

class SquareLoss(Loss):
    def __init__(self): pass

    def loss(self, y, y_pred):
        judge_type(y)
        judge_type(y_pred)
        return 0.5 * cupy.power((y - y_pred), 2)

    def gradient(self, y, y_pred):
        y = cupy.asarray(y, dtype=float)
        y_pred = cupy.asarray(y_pred, dtype=float)
        return -(y - y_pred)

class CrossEntropy(Loss):
    def __init__(self): pass

    def loss(self, y, p):
        # Avoid division by zero
        judge_type(y)
        judge_type(p)
        p = cupy.clip(p, 1e-15, 1 - 1e-15)
        return - y * cupy.log(p) - (1 - y) * cupy.log(1 - p)

    def acc(self, y, p):
        judge_type(y)
        judge_type(p)
        return accuracy_score(cupy.argmax(y, axis=1), cupy.argmax(p, axis=1))

    def gradient(self, y, p):
        # Avoid division by zero
        judge_type(y)
        judge_type(p)
        p = cupy.clip(p, 1e-15, 1 - 1e-15)
        return - (y / p) + (1 - y) / (1 - p)