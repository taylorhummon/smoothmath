from pytest import approx, raises
import math
from smoothmath import DomainError, Point
from smoothmath.expression import (
    Variable, Constant, Negation, Multiply, Reciprocal, NthPower, Exponential, Logarithm
)
from assert_derivatives import ( # type: ignore
    assert_1_ary_derivatives,
    assert_1_ary_derivatives_raise
)


def test_Logarithm():
    x = Variable("x")
    z = Logarithm(x)
    # at x = 1
    point = Point(x = 1)
    assert z.at(point) == approx(0)
    assert_1_ary_derivatives(z, point, x, 1)
    # at x = e
    point = Point(x = math.e)
    assert z.at(point) == approx(1)
    assert_1_ary_derivatives(z, point, x, 1 / math.e)
    # at x = 0
    point = Point(x = 0)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_derivatives_raise(z, point, x)
    # at x = -1
    point = Point(x = -1)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_derivatives_raise(z, point, x)


def test_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(3))
    point = Point(x = 2)
    assert z.at(point) == approx(0)
    assert_1_ary_derivatives(z, point, x, 2)


def test_base_two_Logarithm():
    x = Variable("x")
    z = Logarithm(x, base = 2)
    # at x = 1
    point = Point(x = 1)
    assert z.at(point) == approx(0)
    assert_1_ary_derivatives(z, point, x, 1.442695040888)
    # at x = 2
    point = Point(x = 2)
    assert z.at(point) == approx(1)
    assert_1_ary_derivatives(z, point, x, 0.721347520444)
    # at x = 0
    point = Point(x = 0)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_derivatives_raise(z, point, x)
    # at x = -1
    point = Point(x = -1)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_derivatives_raise(z, point, x)


def test_base_two_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(6), base = 2)
    point = Point(x = 7)
    assert z.at(point) == approx(3)
    assert_1_ary_derivatives(z, point, x, 0.3606737602222)


def test_Logarithm_equality():
    x = Variable("x")
    y = Variable("y")
    assert Logarithm(x) == Logarithm(x)
    assert Logarithm(x) != Logarithm(y)
    assert Logarithm(x) == Logarithm(x, base = math.e)
    assert Logarithm(x, base = 2) == Logarithm(x, base = 2)
    assert Logarithm(x, base = 2) != Logarithm(x, base = 3)
    assert Logarithm(x, base = 2) != Logarithm(x)


def test_Logarithm_normalization():
    x = Variable("x")
    y = Variable("y")
    z = Logarithm(x)
    assert z._normalize() == Logarithm(x)
    z = Logarithm(Exponential(x))
    assert z._normalize() == x
    z = Logarithm(Exponential(x, base = 2), base = 2)
    assert z._normalize() == x
    z = Logarithm(Exponential(x, base = 3), base = 2)
    assert z._normalize() == Logarithm(Exponential(x, base = 3), base = 2)
    z = Logarithm(Reciprocal(x))
    assert z._normalize() == Negation(Logarithm(x))
    z = Logarithm(Reciprocal(x), base = 2)
    assert z._normalize() == Negation(Logarithm(x, base = 2))
    z = Logarithm(NthPower(x, n = 3))
    assert z._normalize() == Constant(3) * Logarithm(x)
    z = Logarithm(NthPower(x, n = 3), base = 2)
    assert z._normalize() == Constant(3) * Logarithm(x, base = 2)
    z = Logarithm(NthPower(x, n = 4))
    # We don't want to reduce to Multiply(Constant(4), Logarithm(u)) because u might be negative
    assert z._normalize() == Logarithm(NthPower(x, n = 4))
    z = Logarithm(Multiply(x, y))
    assert z._normalize() == Logarithm(Multiply(x, y))
