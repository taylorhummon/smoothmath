from pytest import approx
import math
from smoothmath import Point
from smoothmath.expression import Variable, Constant, Negation, Reciprocal, Exponential, Logarithm
from assert_derivatives import assert_1_ary_derivatives # type: ignore


def test_Exponential():
    x = Variable("x")
    z = Exponential(x)
    # at x = 0
    point = Point(x = 0)
    assert z.evaluate(point) == approx(1)
    assert_1_ary_derivatives(z, point, x, 1)
    # at x = 1
    point = Point(x = 1)
    assert z.evaluate(point) == approx(math.e)
    assert_1_ary_derivatives(z, point, x, math.e)
    # at x = -1
    point = Point(x = -1)
    assert z.evaluate(point) == approx(1 / math.e)
    assert_1_ary_derivatives(z, point, x, 1 / math.e)


def test_Exponential_composition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(6))
    point = Point(x = 3)
    assert z.evaluate(point) == approx(1)
    assert_1_ary_derivatives(z, point, x, 2)


def test_base_two_Exponential():
    x = Variable("x")
    z = Exponential(x, base = 2)
    # at x = 0
    point = Point(x = 0)
    assert z.evaluate(point) == approx(1)
    assert_1_ary_derivatives(z, point, x, 0.693147180559)
    # at x = 1
    point = Point(x = 1)
    assert z.evaluate(point) == approx(2)
    assert_1_ary_derivatives(z, point, x, 1.386294361119)
    # at x = -1
    point = Point(x = -1)
    assert z.evaluate(point) == approx(0.5)
    assert_1_ary_derivatives(z, point, x, 0.346573590279)


def test_base_two_Exponential_composition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(5), base = 2)
    point = Point(x = 3)
    assert z.evaluate(point) == approx(2)
    assert_1_ary_derivatives(z, point, x, 2.77258872223)


def test_Exponential_equality():
    x = Variable("x")
    y = Variable("y")
    assert Exponential(x) == Exponential(x)
    assert Exponential(x) != Exponential(y)
    assert Exponential(x) == Exponential(x, base = math.e)
    assert Exponential(x, base = 2) == Exponential(x, base = 2)
    assert Exponential(x, base = 2) != Exponential(x, base = 3)
    assert Exponential(x, base = 2) != Exponential(x)


def test_Exponential_normalization():
    x = Variable("x")
    y = Variable("y")
    z = Exponential(x)
    assert z._normalize() == Exponential(x)
    z = Exponential(Logarithm(x))
    assert z._normalize() == x
    z = Exponential(Logarithm(x, base = 2), base = 2)
    assert z._normalize() == x
    z = Exponential(Logarithm(x, base = 3), base = 2)
    assert z._normalize() == Exponential(Logarithm(x, base = 3), base = 2)
    z = Exponential(Negation(x))
    assert z._normalize() == Reciprocal(Exponential(x))
    z = Exponential(Negation(x), base = 2)
    assert z._normalize() == Reciprocal(Exponential(x, base = 2))
    z = Exponential(x + y)
    assert z._normalize() == Exponential(x + y)
