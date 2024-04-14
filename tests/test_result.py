from pytest import raises
from araceae.types.result import Result, Ok, Err, or_err
from typing import runtime_checkable, Protocol


@runtime_checkable
class _checkable_result(Result, Protocol): ...


def get_ok() -> Result[int]:
    return Ok(100)


def get_err() -> Result[int]:
    return Err("Failed")


def test_result() -> None:
    ok = get_ok()
    err = get_err()

    match ok:
        case Ok(v):
            assert ok.ok
            assert v == 100
        case Err(c):
            raise Exception(c)

    match err:
        case Ok(_):
            assert False, "This was unexpected"
        case Err(c):
            assert not err.ok
            with raises(TypeError):
                print(err.value)


def test_proto():
    ok = get_ok()
    err = get_err()

    assert isinstance(ok, _checkable_result)
    assert isinstance(ok, Ok)
    assert not isinstance(ok, Err)
    assert isinstance(err, _checkable_result)
    assert isinstance(err, Err)
    assert not isinstance(err, Ok)


def test_methods_and_functions():
    ok = get_ok()
    err = get_err()

    assert ok.or_raise() == 100

    with raises(Exception):
        err.or_raise()

    with raises(MemoryError):
        err.or_raise(MemoryError("Oh oh"))

    assert ok.or_none() is not None
    assert err.or_none() is None

    assert not or_err(None).ok
    assert or_err(123).ok
