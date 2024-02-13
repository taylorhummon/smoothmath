from pytest import approx
from smoothmath import Point
from smoothmath.expression import (
    Variable, Constant, Negation, Reciprocal, NthPower, NthRoot, Exponential
)
from assert_derivatives import assert_1_ary_derivatives # type: ignore


def test_NthPower_with_n_equal_two():
    x = Variable("x")
    z = NthPower(x, n = 2)
    # at x = 3
    point = Point(x = 3)
    assert z.evaluate(point) == approx(9)
    assert_1_ary_derivatives(z, point, x, 6)
    # at x = 0
    point = Point(x = 0)
    assert z.evaluate(point) == approx(0)
    assert_1_ary_derivatives(z, point, x, 0)
    # at x = -5
    point = Point(x = -5)
    assert z.evaluate(point) == approx(25)
    assert_1_ary_derivatives(z, point, x, -10)


def test_NthPower_with_n_equal_two_composition():
    x = Variable("x")
    z = NthPower(Constant(3) * x - Constant(1), n = 2)
    point = Point(x = 1)
    assert z.evaluate(point) == approx(4)
    assert_1_ary_derivatives(z, point, x, 12)


def test_NthPower_with_n_equal_one():
    x = Variable("x")
    z = NthPower(x, n = 1)
    # at x = 3
    point = Point(x = 3)
    assert z.evaluate(point) == approx(3)
    assert_1_ary_derivatives(z, point, x, 1)
    # at x = 0
    point = Point(x = 0)
    assert z.evaluate(point) == approx(0)
    assert_1_ary_derivatives(z, point, x, 1)
    # at x = -5
    point = Point(x = -5)
    assert z.evaluate(point) == approx(-5)
    assert_1_ary_derivatives(z, point, x, 1)


def test_NthPower_with_n_equal_one_composition():
    x = Variable("x")
    z = NthPower(Constant(3) * x - Constant(1), n = 1)
    point = Point(x = 1)
    assert z.evaluate(point) == approx(2)
    assert_1_ary_derivatives(z, point, x, 3)


def test_NthPower_normalization():
    x = Variable("x")
    z = NthPower(x, n = 1)
    assert z._normalize() == x
    z = NthPower(x, n = 2)
    assert z._normalize() == NthPower(x, n = 2)
    z = NthPower(NthPower(x, n = 3), n = 2)
    assert z._normalize() == NthPower(x, n = 6)
    z = NthPower(NthRoot(x, n = 2), n = 2)
    assert z._normalize() == x
    z = NthPower(NthRoot(x, n = 2), n = 6)
    assert z._normalize() == NthPower(x, n = 3)
    z = NthPower(NthRoot(x, n = 6), n = 2)
    assert z._normalize() == NthRoot(x, n = 3)
    z = NthPower(NthRoot(x, n = 6), n = 4)
    assert z._normalize() == NthPower(NthRoot(x, n = 3), n = 2)
    z = NthPower(NthRoot(x, n = 4), n = 6)
    assert z._normalize() == NthPower(NthRoot(x, n = 2), n = 3)
    z = NthPower(Negation(x), n = 2)
    assert z._normalize() == NthPower(x, n = 2)
    z = NthPower(Negation(x), n = 3)
    assert z._normalize() == Negation(NthPower(x, n = 3))
    z = NthPower(Reciprocal(x), n = 2)
    assert z._normalize() == Reciprocal(NthPower(x, n = 2))
    z = NthPower(Exponential(x), n = 2)
    assert z._normalize() == Exponential(Constant(2) * x)
    z = NthPower(Exponential(x, base = 2), n = 3)
    assert z._normalize() == Exponential(Constant(3) * x, base = 2)
