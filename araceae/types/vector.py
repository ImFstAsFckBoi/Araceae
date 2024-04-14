from typing import Iterator, Tuple, Sequence, overload
from typing_extensions import Self
from math import sqrt, sin, cos
from nptyping import NDArray
import numpy as np


class Vec(Sequence[float]):
    """An Nx1 vector class, supporting common vector operations and can use
    float or integer elements

    Example::

        v = type(self)(1, 2, 3)
        u = v * 5  # u = [5, 10, 15]
        w = type(self)(3, 4)
        x = w.euclidean()  # x = 5.0

    """
    _size: int
    _data: NDArray

    def __init__(self, *rows: float) -> None:
        self._size = len(rows)
        self._data = np.array(rows, dtype=np.float64, copy=True)

    def euclidean(self) -> float:
        return sqrt(np.sum(self._data ** 2))

    def manhattan(self) -> float:
        return np.sum(np.abs(self._data))

    def as_int_t(self) -> Tuple[int, ...]:
        return tuple(map(int, self._data))

    def matmul(self, matrix: NDArray) -> Self:
        assert matrix.shape == (self._size, self._size)
        r = np.matmul(self._data, matrix)
        assert r.shape == (self._size,)
        return type(self)(*r)

    @overload
    def __getitem__(self, key: int) -> float: ...
    @overload
    def __getitem__(self, key: slice) -> Sequence[float]: ...

    def __getitem__(self, key: int | slice) -> Sequence[float] | float:
        if isinstance(key, int):
            if key >= self._size: raise IndexError
            return self._data[key]

        elif isinstance(key, slice):
            if key.stop >= self._size: raise IndexError
            return list(self._data[key])

        return NotImplemented

    def __setitem__(self, key: int, newValue: float) -> None:
        if key >= self._size: raise IndexError
        self._data[key] = newValue

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[float]:
        return iter(self._data)

    def __abs__(self) -> Self:
        return type(self)(*map(abs, self._data))

    def __add__(self, other: Sequence[float]):
        assert self._size == len(other)
        return type(self)(*(self._data + other))

    def __sub__(self, other: Sequence[float]) -> Self:
        assert self._size == len(other)
        return type(self)(*(self._data - other))

    def __mul__(self, mul: float) -> Self:
        return type(self)(*(self._data * mul))

    def __iadd__(self, other: Sequence[float]) -> Self:
        assert self._size == len(other)
        self._data += other
        return self

    def __isub__(self, other: Sequence[float]) -> Self:
        assert self._size == len(other)
        self._data -= other
        return self

    def __imul__(self, mul: float) -> Self:
        self._data *= mul
        return self

    def __lt__(self, other: Self) -> bool:
        assert self._size == other._size
        return self.euclidean() < other.euclidean()

    def __le__(self, other: Self) -> bool:
        assert self._size == other._size
        return self.euclidean() <= other.euclidean()

    def __gt__(self, other: Self) -> bool:
        assert self._size == other._size
        return self.euclidean() > other.euclidean()

    def __ge__(self, other: Self) -> bool:
        assert self._size == other._size
        return self.euclidean() >= other.euclidean()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (Vec, Sequence)):
            assert self._size == len(other)
            return np.array_equal(self, other)
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, (Vec)):
            assert self._size == len(other)
            return not np.array_equal(self, other)
        return NotImplemented

    def __str__(self) -> str:
        return f'Vec{str(self._data)}'

    def __repr__(self) -> str:
        return self.__str__()

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __reversed__(self) -> Iterator[float]:
        return reversed(self._data)


class Vec2(Vec):
    """A 2x1 Vector, based or `Vec` with `x` and `y` properties"""

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)

    @property
    def x(self) -> float: return self._data[0]

    @property
    def y(self) -> float: return self._data[1]


class Vec3(Vec):
    """A 3x1 Vector, based or `Vec` with `x`, `y` and `y` properties"""

    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__(x, y, z)

    @property
    def x(self) -> float: return self._data[0]

    @property
    def y(self) -> float: return self._data[1]

    @property
    def z(self) -> float: return self._data[2]


def euclidean(a: Vec, b: 'Vec') -> float:
    "Euclidean distance between two points"
    return sqrt(sum(map(lambda ab: (ab[0] - ab[1])**2, zip(a, b))))


def manhattan(a: Vec, b: 'Vec') -> float:
    "Manhattan distance between two points"
    return sum(map(lambda ab: abs(ab[0] - ab[1]), zip(a, b)))


def rotation_matrix(rads: float) -> NDArray:
    return np.array([[cos(rads), -sin(rads)],
                     [sin(rads), cos(rads)]], dtype=float)


Point2 = Dim = Vec2
taxi = manhattan
pythagorean = distance = euclidean
