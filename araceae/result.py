from typing import TypeVar, Generic, Optional, Protocol


T = TypeVar('T', covariant=True)


class Result(Generic[T], Protocol):
    @property
    def ok(self) -> bool: ...


class Err:
    cause: str
    ok = False

    __match_args__ = ('cause',)

    def __init__(self, cause: Optional[str] = None):
        self.cause = cause or ''

    @property
    def value(self) -> None:
        raise TypeError('Attempted to grab `value` from object of type `Err`. '
                        'Check that result is type `Ok` using `match`, '
                        '`isinstance` or `Result.ok` first.')


class Ok(Generic[T]):
    value: T
    ok = True

    __match_args__ = ('value',)

    def __init__(self, val: T):
        self.value = val
