from pytest import CaptureFixture
from ..testing.time import s_to_xs, timer
from time import sleep
from typing import Tuple, List


def test_s_to_xs() -> None:
    def _test(v: float, e: Tuple[float, str]):
        r = s_to_xs(v)
        if r[0] >= 1:
            r = (round(r[0]), r[1])
        assert r == e

    values: List[float] = [
        10000,
        1,
        0.123,
        2.8e-5,
        9.9e-8,
        7.0e-12,
        0.2e-12,
        0.2e-13,
    ]

    expected: List[Tuple[float, str]] = [
        (10000, 's'),
        (1, 's'),
        (123, 'ms'),
        (28, 'us'),
        (99, 'ns'),
        (7, 'ps'),
        (0.2, 'ps'),
        (0.02, 'ps'),
    ]

    for v, e in zip(values, expected):
        _test(v, e)


def test_timer(capsys: CaptureFixture[str]):
    with timer('Test1', 0, timer.MODE_DELTA) as _:
        sleep(1)

    with timer('Test2', 0, timer.MODE_HZ) as _:
        sleep(0.5)

    capture = capsys.readouterr()
    assert capture.out.find('Test1: 1.0 s') != -1
    assert capture.out.find('Test2: 2 Hz') != -1
