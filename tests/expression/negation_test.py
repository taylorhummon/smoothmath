from pytest import approx
from smoothmath import Point
from smoothmath.expression import Variable, Constant, Negation
from assert_derivatives import assert_1_ary_derivatives # type: ignore


def test_Negation():
    x = Variable("x")
    z = Negation(x)
    point = Point(x = 2)
    assert z.evaluate(point) == approx(-2)
    assert_1_ary_derivatives(z, point, x, -1)


def test_Negation_composition():
    x = Variable("x")
    z = Negation(Constant(2) * x + Constant(1))
    point = Point(x = 3)
    assert z.evaluate(point) == approx(-7)
    assert_1_ary_derivatives(z, point, x, -2)


def test_Negation_normalization():
    x = Variable("x")
    y = Variable("y")
    z = Negation(x)
    assert z._normalize() == Negation(x)
    z = Negation(Negation(x))
    assert z._normalize() == x
    z = Negation(Negation(Negation(x)))
    assert z._normalize() == Negation(x)
    z = Negation(x + y)
    assert z._normalize() == Negation(x + y)
