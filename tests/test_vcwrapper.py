from araceae.vcwrapper import vccommon, vcfile, vcnull
from typing import runtime_checkable, Protocol
from random import randrange


@runtime_checkable
class check_vccommon(vccommon, Protocol): ...


def test_proto():
    v = vcfile('')
    assert isinstance(v, check_vccommon)
    assert issubclass(vcfile, check_vccommon)


def test_iter():
    x = 0
    y = randrange(0, 100)
    null = vcnull(10, 10, y)
    for i, _ in enumerate(null):
        x = i

    assert x == y - 1
