"""
A collection of utility classes for signal processing.
"""

from typing import Sequence, Any, Union
import numpy as np
from nptyping import NDArray


class FlankDetector:
    """
    Generic utility class for detecting rising or falling edges in signals.
    """
    __low: Sequence[Any]
    __high: Sequence[Any]
    __last: int = 0

    def __init__(self,
                 lows: Union[Any, Sequence[Any]],
                 highs: Union[Any, Sequence[Any]]):
        if hasattr(lows, '__iter__'):
            self.__low = lows
        else:
            self.__low = (lows,)
        if hasattr(highs, '__iter__'):
            self.__high = highs
        else:
            self.__high = (highs,)

    def is_rising(self, value: Any, strict=True) -> bool:
        """Returns True if the supplied value is a logical high
        and the previous value was a logical low.
        Performs `step(value)` implicitly.

        Args:
            value (Any): Any value defined as low or high
            when class was initialized.

            strict (bool, optional): Raise Exception if value not in either
            low or high. Skips step if False and value in undefined.
            Defaults to True.

        Raises:
            ValueError: If strict and value is undefined.

        Returns:
            bool: If signal goes from low to high.
        """
        if self.__last == 0:
            return self.step(value, strict) == 1
        self.step(value, strict)
        return False

    def is_falling(self, value: Any, strict=True) -> bool:
        """Returns True if the supplied value is a logical low
        and the previous value was a logical high.
        Performs `step(value)` implicitly.

        Args:
            value (Any): Any value defined as low or high
            when class was initialized.

            strict (bool, optional): Raise Exception if value not in either
            low or high. Skips step if False and value in undefined.
            Defaults to True.

        Raises:
            ValueError: If strict and value is undefined.

        Returns:
            bool: If signal goes from high to low.
        """
        if self.__last == 1:
            return self.step(value, strict) == 0
        self.step(value, strict)
        return False

    def rising_or_falling(self, value: Any, strict=True) -> Union[bool, None]:
        """Look for both rising and falling edged.

        Args:
            value (Any): Any value defined as low or high.
            strict (bool, optional): Raise Exception if value not in either
            low or high. Skips step if False and value in undefined.
            Defaults to True.

        Returns:
            Optional[bool]: Returns True if rising edge, False if falling edge
            or None if neither.
        """
        last = self.__last
        step = self.step(value, strict)

        if last == 0 and step == 1: return True
        if last == 1 and step == 0: return False
        else: return None

    def step(self, value: Any, strict=True) -> Union[int, None]:
        """Process next signal value and return values logical value, either
        low (0) or high (1)

        Args:
            value (Any): Any value defined as low or high
            when class was initialized.

            strict (bool, optional): Raise Exception if value not in either
            low or high. Skips step if False and value in undefined.
            Defaults to True.

        Raises:
            ValueError: If strict and value is undefined.

        Returns:
            int: Signals logical value (0 or 1 for low or high).
        """
        if value in self.__low:
            self.__last = 0
            return self.__last
        elif value in self.__high:
            self.__last = 1
            return self.__last

        if strict:
            raise ValueError('Value given which has not specified logical value.')  # noqa: E501

        return None


class Filter:
    value: Union[int, float] = 0
    lock: bool = False

    def __init__(self):
        raise NotImplementedError()

    def __call__(self, value: float) -> float:
        raise NotImplementedError()


class SMAFilter(Filter):
    """Simple Moving Average (SMA) filter
    https://en.wikipedia.org/wiki/Moving_average#Simple_moving_average"""
    __memory: NDArray

    def __init__(self, n: int, init: float = 0):
        """Init filter

        Args:
            n (int): Length of the filter.
            init (int | float, optional): Initial value to fill the filter
            history with. Defaults to 0.
        """
        self.__memory = np.full((n), init, dtype=float)
        self.lock = False

    def __call__(self, v: float) -> float:
        """Processing the next signal value and get the new filter value.

        Args:
            v (int | float): Newest signal value to be processed.
            Can be Any numerical value.

        Returns:
            float: Filters new value.
        """
        if not self.lock:
            self.__memory = np.roll(self.__memory, 1, axis=0)
            self.__memory[0] = v
            self.value = float(np.average(self.__memory))
        return self.value


class FIRFilter(Filter):
    """Simple Finite Impulse Response (FIR) filter implementation.
    https://en.wikipedia.org/wiki/Finite_impulse_response"""
    __memory: NDArray
    __weights: NDArray

    def __init__(self,
                 weights: Union[Sequence[float], NDArray],
                 init: float = 0):
        """Init filter

        Args:
            weights (Sequence[float  |  int]): Filter weights. Filter length
            will be equal to the filters length.
            init (int | float, optional): Initial value to fill the filter
            history with. Defaults to 0.

        Raises:
            ValueError: Invalid weight array.
        """
        self.__weights = np.array(weights)
        s = self.__weights.shape
        if len(s) > 1: raise ValueError('Weights must be a 1D array.')

        self.__memory = np.full_like(weights, init, dtype=float)
        self.lock = False

    def __call__(self, v: float) -> float:
        """Processing the next signal value and get the new filter value.

        Args:
            v (int | float): Newest signal value to be processed.
            Can be Any numerical value.

        Returns:
            float: Filters new value.
        """
        if not self.lock:
            self.__memory = np.roll(self.__memory, 1, axis=0)
            self.__memory[0] = v
            self.value = float(np.sum(self.__memory * self.__weights))
        return self.value
