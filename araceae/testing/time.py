from ..console import println
from typing import Tuple
from time import time

_xs = ['s', 'ms', 'us', 'ns', 'ps']


def s_to_xs(s: float) -> Tuple[float, str]:
    """Auto convert time to most appropriate unit.
    Ranged from seconds (s) to pico seconds (ps).
    Return: (value: float, unit: str)

    Example::

        s_to_xs(0.023)  # = (23, 'ms')
    """
    for f in _xs:
        if s >= 1:
            return (s, f)
        s *= 1000

    return s/1000, _xs[-1]


class timer:
    MODE_DELTA = 0
    MODE_HZ = 1
    __start = 0
    __label = ''
    __mode = ''
    __decimals = 2

    def __init__(self, label: str = 'Timer',
                 decimals: int = 2,
                 mode=MODE_DELTA):
        self.__start = time()
        self.__label = label
        self.__mode = mode
        self.__decimals = decimals

    def __enter__(self):
        return None

    def __exit__(self, type, value, traceback):
        if self.__mode == timer.MODE_DELTA:
            s, f = s_to_xs(time()-self.__start)
            println(f'{self.__label}: {round(s, self.__decimals)} {f}')
        elif self.__mode == timer.MODE_HZ:
            println(f'{self.__label}: {round(1/(time()-self.__start))} Hz')
