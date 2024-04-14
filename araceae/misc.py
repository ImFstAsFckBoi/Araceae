"""A collection of miscellaneous utilities."""

import numpy as np


def clamp(v: float, _min: float, _max: float) -> float:
    """Clamp the value of `v` between `_min` and `_max`"""
    return max(_min, min(_max, v))


vclamp = np.vectorize(clamp, excluded=("_min", "_max"))
