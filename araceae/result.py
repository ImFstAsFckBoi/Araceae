from typing import TypeVar, Generic, Optional, Union


T = TypeVar('T')


class Err:
    cause: str

    def __init__(self, cause: Optional[str] = None):
        self.cause = cause or ''


class Ok(Generic[T]):
    value: T

    def __init__(self, val: T):
        self.value = val


Result = Union[Ok[T], Err]
