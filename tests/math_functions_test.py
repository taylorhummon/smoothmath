from pytest import raises, approx
import math
from smoothmath import DomainError
from smoothmath._private.math_functions import (
    add, minus, negation,
    multiply, divide, reciprocal,
    power, nth_power, nth_root, exponential, logarithm,
    cosine, sine
)


def test_add():
    assert add(4, 5) == approx(9)
    assert add(4, 5, 6) == approx(15)
    assert add(4) == approx(4)
    assert add() == approx(0)


def test_minus():
    assert minus(5, 2) == approx(3)


def test_negation():
    assert negation(5) == approx(-5)
    assert negation(-5) == approx(5)
    assert negation(0) == approx(0)


def test_multiply():
    assert multiply(4, 5) == approx(20)
    assert multiply(4, 5, 6) == approx(120)
    assert multiply(4, 0, 6) == approx(0)
    assert multiply(4) == approx(4)
    assert multiply() == approx(1)


def test_divide():
    assert divide(6, 3) == approx(2)
    assert divide(1, 2) == approx(0.5)
    assert divide(0, 2) == approx(0)
    with raises(DomainError):
        divide(2, 0)
    with raises(DomainError):
        divide(0, 0)


def test_reciprocal():
    assert reciprocal(2) == approx(0.5)
    assert reciprocal(0.5) == approx(2)
    assert reciprocal(-5) == approx(-0.2)
    with raises(DomainError):
        reciprocal(0)


def test_power():
    assert power(2, 3) == approx(8)
    assert power(3, 2) == approx(9)
    assert power(9, 0.5) == approx(3)
    assert power(5, -1) == approx(0.2)
    with raises(DomainError):
        power(0, 2)
    with raises(DomainError):
        power(0, -2)
    with raises(DomainError):
        power(0, 0)
    with raises(DomainError):
        power(-2, 2)


def test_nth_power():
    # n = -1
    with raises(DomainError):
        nth_power(3, -1)
    # n = 0
    with raises(DomainError):
        nth_power(3, 0)
    # n = 1
    assert nth_power(0, 1) == approx(0)
    assert nth_power(3, 1) == approx(3)
    assert nth_power(-3, 1) == approx(-3)
    assert nth_power(0.5, 1) == approx(0.5)
    # n = 2
    assert nth_power(0, 2) == approx(0)
    assert nth_power(3, 2) == approx(9)
    assert nth_power(-3, 2) == approx(9)
    assert nth_power(0.5, 2) == approx(0.25)
    # n = 3
    assert nth_power(0, 3) == approx(0)
    assert nth_power(3, 3) == approx(27)
    assert nth_power(-3, 3) == approx(-27)
    assert nth_power(0.5, 3) == approx(0.125)


def test_nth_root():
    # n = -1
    with raises(DomainError):
        nth_root(12, -1)
    # n = 0
    with raises(DomainError):
        nth_root(12, 0)
    # n = 1
    assert nth_root(0.5, 1) == approx(0.5)
    assert nth_root(1, 1) == approx(1)
    assert nth_root(2, 1) == approx(2)
    assert nth_root(0, 1) == approx(0)
    assert nth_root(-0.5, 1) == approx(-0.5)
    assert nth_root(-1, 1) == approx(-1)
    assert nth_root(-2, 1) == approx(-2)
    # n = 2 (a.k.a square root)
    assert nth_root(0.25, 2) == approx(0.5)
    assert nth_root(1, 2) == approx(1)
    assert nth_root(2, 2) == approx(1.4142135623730)
    assert nth_root(9, 2) == approx(3)
    assert nth_root(50 ** 2, 2) == approx(50)
    with raises(DomainError):
        nth_root(0, 2)
    with raises(DomainError):
        nth_root(-1, 2)
    # n = 3 (a.k.a cube root)
    assert nth_root(0.125, 3) == approx(0.5)
    assert nth_root(1, 3) == approx(1)
    assert nth_root(2, 3) == approx(1.2599210498948)
    assert nth_root(8, 3) == approx(2)
    assert nth_root(50 ** 3, 3) == approx(50)
    with raises(DomainError):
        nth_root(0, 3)
    assert nth_root(-0.125, 3) == approx(-0.5)
    assert nth_root(-1, 3) == approx(-1)
    assert nth_root(-2, 3) == approx(-1.2599210498948)
    assert nth_root(-8, 3) == approx(-2)
    # n = 4
    assert nth_root(0.5 ** 4, 4) == approx(0.5)
    assert nth_root(1, 4) == approx(1)
    assert nth_root(4, 4) == approx(1.4142135623730)
    assert nth_root(81, 4) == approx(3)
    assert nth_root(50 ** 4, 4) == approx(50)
    with raises(DomainError):
        nth_root(0, 4)
    with raises(DomainError):
        nth_root(-1, 4)
    # n = 5
    assert nth_root(0.5 ** 5, 5) == approx(0.5)
    assert nth_root(1, 5) == approx(1)
    assert nth_root(4, 5) == approx(1.3195079107728942)
    assert nth_root(243, 5) == approx(3)
    assert nth_root(50 ** 5, 5) == approx(50)
    with raises(DomainError):
        nth_root(0, 5)
    assert nth_root(-1, 5) == approx(-1)
    assert nth_root(-243, 5) == approx(-3)


def test_exponential():
    # base = -1
    with raises(DomainError):
        exponential(3, base = -1)
    # base = 0
    with raises(DomainError):
        exponential(3, base = 0)
    # base = 1
    assert exponential(3, base = 1) == approx(1)
    # base = 2
    assert exponential(3, base = 2) == approx(8)
    assert exponential(1, base = 2) == approx(2)
    assert exponential(0, base = 2) == approx(1)
    assert exponential(-2, base = 2) == approx(0.25)
    # default base: e
    assert exponential(3) == approx(math.e * math.e * math.e)
    assert exponential(1) == approx(math.e)
    assert exponential(0) == approx(1)
    assert exponential(-2) == approx(1 / (math.e * math.e))


def test_logarithm():
    # base = -1
    with raises(DomainError):
        logarithm(1, base = -1)
    # base = 0
    with raises(DomainError):
        logarithm(1, base = 0)
    # base = 1
    with raises(DomainError):
        logarithm(1, base = 1)
    # base = 2
    assert logarithm(8, base = 2) == approx(3)
    assert logarithm(2, base = 2) == approx(1)
    assert logarithm(1, base = 2) == approx(0)
    assert logarithm(0.25, base = 2) == approx(-2)
    # default base: e
    assert logarithm(math.e * math.e * math.e) == approx(3)
    assert logarithm(math.e) == approx(1)
    assert logarithm(1) == approx(0)
    assert logarithm(1 / (math.e * math.e)) == approx(-2)


def test_cosine():
    assert cosine(math.tau) == approx(1)
    assert cosine(math.tau / 2) == approx(-1)
    assert cosine(math.tau / 4) == approx(0)
    assert cosine(0) == approx(1)
    assert cosine(math.tau / 4) == approx(0)
    assert cosine(- math.tau / 2) == approx(-1)
    assert cosine(- math.tau) == approx(1)


def test_sine():
    assert sine(math.tau) == approx(0)
    assert sine(math.tau / 2) == approx(0)
    assert sine(math.tau / 4) == approx(1)
    assert sine(0) == approx(0)
    assert sine(- math.tau / 4) == approx(-1)
    assert sine(- math.tau / 2) == approx(0)
    assert sine(- math.tau) == approx(0)
