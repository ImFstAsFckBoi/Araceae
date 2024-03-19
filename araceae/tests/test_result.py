from araceae.result import Result, Ok, Err
from pytest import raises


def get_ok() -> Result[int]:
    return Ok(100)


def get_err() -> Result[int]:
    return Err("Failed")


def test_result() -> None:
    x = get_ok()

    match x:
        case Ok(v):
            assert x.ok
            assert v == 100
        case Err(c):
            raise Exception(c)

    y = get_err()

    match y:
        case Ok(_):
            assert False, "This was unexpected"
        case Err(c):
            assert not y.ok
            with raises(TypeError):
                print(y.value)
