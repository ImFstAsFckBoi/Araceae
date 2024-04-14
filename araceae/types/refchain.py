from typing import TypeVar, Generic

_T2 = TypeVar("_T2")


class RefChain(Generic[_T2]):
    _value: _T2 | None
    _next: "RefChain[_T2] | None"
    _end: bool

    def __init__(self, value: "_T2 | RefChain[_T2]") -> None:
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

    def get_end(self) -> "RefChain[_T2]":
        c = self
        while True:
            if c._end:
                break
            assert c._next
            c = c._next
        return c

    def move_end(self, next: "RefChain[_T2]") -> None:
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
        return f"{id(self)} -> {self._next.__str__()}"

    def __repr__(self) -> str:
        return self.__str__()
