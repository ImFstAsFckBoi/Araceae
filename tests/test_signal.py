from araceae.signal import FlankDetector as FD, SMAFilter, FIRFilter
from pytest import raises
from numpy import array


def test_flank1():
    fd = FD((1, 3, 5), (2, 4, 6))
    fd.step(1)

    assert fd.is_rising(4)

    with raises(ValueError):
        fd.step(8)

    try:
        fd.step(8, False)
    except ValueError:
        assert False

    assert fd.step(3) == 0
    assert not fd.is_falling(2)
    assert fd.is_falling(5)
    fd.step(8, False)
    assert fd.is_rising(6)
    assert not fd.is_falling(6)
    assert fd.is_falling(1)
    assert fd.is_rising(2)


def test_flank2():
    fd = FD(0, 1)
    assert fd.step(0) == 0
    assert fd.step(1) == 1


def test_SMA():
    filt = SMAFilter(3)

    assert filt(3) == 3/3
    assert filt(3) == 6/3
    assert filt(3) == 9/3
    assert filt(2) == 8/3
    assert filt(5) == 10/3
    assert filt(0) == 7/3
    assert filt(0) == 5/3
    assert filt(0) == 0/3


def test_FIR():
    w = array([1, 2, 3]) / 3
    filt = FIRFilter(w)

    assert filt(2) == 2/3
    assert filt(0) == 4/3
    assert filt(0) == 6/3
    assert filt(3) == 3/3
    assert filt(3) == 9/3
    assert filt(3) == 18/3
    assert filt(0) == 15/3
    assert filt(0) == 9/3
    assert filt(0) == 0/3


def test_FIR2():
    fir = FIRFilter([1/3, 1/3, 1/3], 7)
    sma = SMAFilter(3, 7)

    assert round(fir(3), 3) == round(sma(3), 3)
    assert round(fir(3), 3) == round(sma(3), 3)
    assert round(fir(3), 3) == round(sma(3), 3)
    assert round(fir(2), 3) == round(sma(2), 3)
    assert round(fir(5), 3) == round(sma(5), 3)
    assert round(fir(0), 3) == round(sma(0), 3)
    assert round(fir(0), 3) == round(sma(0), 3)
    assert round(fir(0), 3) == round(sma(0), 3)
