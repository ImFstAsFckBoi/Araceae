from typing import TypeVar, Generic, Optional, Protocol
from typing_extensions import Never


T = TypeVar("T", covariant=True)


class Result(Generic[T], Protocol):
    """Result type which could be either Ok or Err"""

    @property
    def ok(self) -> bool: ...

    def or_raise(
        self,
        exc: Exception | type[Exception] = ...,  # noqa: E501
    ) -> T:
        """Get the value or raise the `exc` exception if the Result is Err"""
        ...

    def or_none(self) -> T | None:
        """Get the value or None is the Result is Err"""
        ...


class Ok(Result, Generic[T]):
    """Positive result, containing a valid result value"""

    value: T

    __match_args__ = ("value",)

    def __init__(self, val: T):
        self.value = val

    @property
    def ok(self):
        return True

    def or_raise(self, exc=...) -> T:
        return self.value

    def or_none(self) -> T | None:
        return self.value


class Err(Result):
    """Negative result, not containing a valid result value"""

    cause: str

    __match_args__ = ("cause",)

    def __init__(self, cause: Optional[str] = None):
        self.cause = cause or ""

    @property
    def ok(self):
        return False

    @property
    def value(self) -> None:
        raise TypeError(
            "Attempted to grab `value` from object of type `Err`. "
            "Check that result is type `Ok` using `match`, "
            "`isinstance` or `Result.ok` first."
        )

    def or_raise(
        self, exc=TypeError("'or_raise' was called on Result with 'Err' type.")
    ) -> Never:
        raise exc

    def or_none(self) -> None:
        return None


def or_err(value: Optional[T]) -> Ok[T] | Err:
    if value is None:
        return Err("Value was None")
    else:
        return Ok(value)
