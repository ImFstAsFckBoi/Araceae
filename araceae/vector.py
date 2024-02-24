from typing import Iterator, List, Tuple
from typing_extensions import Self
from math import sqrt
from nptyping import NDArray
from numpy import matmul


class Vec:
    """An Nx1 vector class, supporting common vector operations and can use
    float or integer elements

    Example::

        v = type(self)(1, 2, 3)
        u = v * 5  # u = [5, 10, 15]
        w = type(self)(3, 4)
        x = w.euclidean()  # x = 5.0

    """
    __size: int
    __data: List[float]
    __count = 0  # Only used for iteration

    def __init__(self, *rows: float) -> None:
        self.__size = len(rows)
        self.__data = [*rows]

    def euclidean(self) -> float:
        return sqrt(sum(map(lambda x: x**2, self)))

    def manhattan(self) -> float:
        return sum(map(abs, self.__data))

    def as_int_t(self) -> Tuple[int, ...]:
        return tuple(map(int, self.__data))

    def matmul(self, matrix: NDArray) -> Self:
        assert matrix.shape == (self.__size, self.__size)
        r = matmul(self.__data, matrix)
        assert r.shape == (self.__size,)
        return type(self)(*r[:])

    def __getitem__(self, key: int) -> float:
        if key >= self.__size: raise IndexError
        return self.__data[key]

    def __setitem__(self, key: int, newValue: float) -> None:
        if key >= self.__size: raise IndexError
        self.__data[key] = newValue

    def __len__(self) -> int:
        return self.__size

    def __iter__(self) -> Iterator[float]:
        return iter(self.__data)

    def __abs__(self) -> Self:
        return type(self)(*map(abs, self.__data))

    def __add__(self, other: Self):
        assert self.__size == other.__size
        return type(self)(*[r1 + r2 for r1, r2 in zip(self, other)])

    def __sub__(self, other: Self) -> Self:
        assert self.__size == other.__size
        return type(self)(*[r1 - r2 for r1, r2 in zip(self, other)])

    def __mul__(self, mul) -> Self:
        return type(self)(*[r * mul for r in self])

    def __iadd__(self, other: Self) -> Self:
        assert self.__size == other.__size
        for s, o in zip(self, other):
            s += o
        return self

    def __isub__(self, other: Self) -> Self:
        assert self.__size == other.__size
        for s, o in zip(self.__data, other):
            s -= o
        return self

    def __imul__(self, mul) -> Self:
        for s in self:
            s *= mul
        return self

    def __lt__(self, other: 'Vec') -> bool:
        assert self.__size == other.__size
        return self.euclidean() < other.euclidean()

    def __le__(self, other: 'Vec') -> bool:
        assert self.__size == other.__size
        return self.euclidean() <= other.euclidean()

    def __gt__(self, other: 'Vec') -> bool:
        assert self.__size == other.__size
        return self.euclidean() > other.euclidean()

    def __ge__(self, other: 'Vec') -> bool:
        assert self.__size == other.__size
        return self.euclidean() >= other.euclidean()

    def __eq__(self, other: 'Vec') -> bool:
        assert self.__size == other.__size
        return sum(map(lambda so: so[0] == so[1], zip(self, other))) != 0

    def __ne__(self, other: 'Vec') -> bool:
        assert self.__size == other.__size
        return sum(map(lambda so: so[0] == so[1], zip(self, other))) == 0

    def __str__(self) -> str:
        return f'Vec{str(self.__data)}'

    def __repr__(self) -> str:
        return self.__str__()


class Vec2(Vec):
    """A 2x1 Vector, based or `Vec` with `x` and `y` properties"""

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)

    @property
    def x(self) -> float: return self.__data[0]

    @property
    def y(self) -> float: return self.__data[1]


class Vec3(Vec):
    """A 3x1 Vector, based or `Vec` with `x`, `y` and `y` properties"""

    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__(x, y, z)


def euclidean(a: Vec, b: 'Vec') -> float:
    "Euclidean distance between two points"
    return sqrt(sum(map(lambda ab: (ab[0] - ab[1])**2, zip(a, b))))


def manhattan(a: Vec, b: 'Vec') -> float:
    "Manhattan distance between two points"
    return sum(map(lambda ab: abs(ab[0] - ab[1]), zip(a, b)))


Point2 = Dim = Vec2
taxi = manhattan
pythagorean = distance = euclidean
