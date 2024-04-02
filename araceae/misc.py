"""A collection of miscellaneous utilities."""
import numpy as np
from typing import TypeVar, Generic


def clamp(v: float, _min: float, _max: float) -> float:
    """Clamp the value of `v` between `_min` and `_max`"""
    return max(_min, min(_max, v))


vclamp = np.vectorize(clamp, excluded=('_min', '_max'))


class iota():
    """Auto incrementing value, similar to iota in Golang.

    Normal usage::

        _iota = iota()
        a = _iota()     # a = 0
        b = _iota()     # b = 1

    Custom values::

        _iota = iota(100, 10)
        a = _iota()     # a = 100
        b = _iota()     # b = 110
    """
    x: int

    def __init__(self, s: int = 0, i: int = 1) -> None:
        """
        Args:
            s (int, optional): Start value. Defaults to 0.
            i (int, optional): Step value. Defaults to 1.
        """
        self.x = s

    def __call__(self) -> int:
        self.x += 1
        return self.x


auto = iota()


_T2 = TypeVar('_T2')


class RefChain(Generic[_T2]):
    _value: _T2 | None
    _next: 'RefChain[_T2] | None'
    _end: bool

    def __init__(self, value: '_T2 | RefChain[_T2]') -> None:
        if isinstance(value, RefChain):
            self._value = None
            self._next = value
            self._end = False
        else:
            self._value = value
            self._next = None
            self._end = True

    def set(self, value: _T2) -> None:
        if self._end:
            assert self._value
            self._value = value
        else:
            assert self._next
            self._next.set(value)

    def get(self) -> _T2:
        if self._end:
            assert self._value
            return self._value
        assert self._next
        return self._next.get()

    def is_end(self) -> bool:
        return self._end

    def get_end(self) -> 'RefChain[_T2]':
        c = self
        while True:
            if c._end: break
            assert c._next
            c = c._next
        return c

    def move_end(self, next: 'RefChain[_T2]') -> None:
        assert self is not next
        end = self.get_end()
        end._value = None
        end._next = next
        end._end = False

    def __str__(self) -> str:
        if self._end:
            assert self._value
            return self._value.__str__()
        assert self._next
        return f'{id(self)} -> {self._next.__str__()}'

    def __repr__(self) -> str:
        return self.__str__()
