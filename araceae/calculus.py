"""
Some utility classes for numerically
approximating calculus functions (integrals and derivatives)
"""


class Integrator:
    """Discrete/Numerical integration using trapezoid rule approximation."""
    __sum: float
    __last: float

    def __init__(self, init: float = 0):
        self.__sum = init
        self.__last = init

    def next(self, y: float, dx: float) -> float:
        self.__sum += dx * (y + (self.__last - y) / 2)
        self.__last = y
        return self.__sum

    @property
    def value(self):
        return self.__sum


class Derivator:
    """Discrete/Numerical derivation using backward finite difference."""
    __last: float
    __saved: float

    def __init__(self, init: float = 0):
        self.__last = init
        self.__saved = init

    def next(self, y: float, dx: float) -> float:
        self.__saved = (self.__last - y) / dx
        self.__last = y
        return self.__saved

    @property
    def value(self) -> float:
        return self.__saved
