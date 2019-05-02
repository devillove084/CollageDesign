import numpy as np
import cupy


def linear_kernel(**kwargs):
    def f(x1, x2):
        return cupy.inner(x1, x2)
    return f


def polynomial_kernel(power, coef, **kwargs):
    def f(x1, x2):
        return (cupy.inner(x1, x2) + coef)**power
    return f


def rbf_kernel(gamma, **kwargs):
    def f(x1, x2):
        distance = cupy.linalg.norm(x1 - x2) ** 2
        return cupy.exp(-gamma * distance)
    return f
