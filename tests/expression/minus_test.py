from pytest import approx
from smoothmath import Point
from smoothmath.expression import Variable, Constant, Minus, Negation
from assert_partials import assert_2_ary_partials # type: ignore


def test_Minus():
    x = Variable("x")
    y = Variable("y")
    z = Minus(x, y)
    point = Point(x = 2, y = 3)
    assert z.at(point) == approx(-1)
    assert_2_ary_partials(z, point, x, 1, y, -1)


def test_Minus_composition():
    x = Variable("x")
    y = Variable("y")
    z = Minus(Constant(5) * x, Constant(4) * y)
    point = Point(x = 2, y = 3)
    assert z.at(point) == approx(-2)
    assert_2_ary_partials(z, point, x, 5, y, -4)


def test_Minus_normalization():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Minus(x, y)
    assert z._normalize() == Minus(x, y)
    z = Minus(x, Constant(0))
    assert z._normalize() == x
    z = Minus(Constant(0), x)
    assert z._normalize() == Negation(x)
    z = Minus(w + x, y)
    assert z._normalize() == Minus(w + x, y)
    z = Minus(w, x + y)
    assert z._normalize() == Minus(w, x + y)
    z = Minus(Minus(w, x), y)
    assert z._normalize() == Minus(w, x + y)
    z = Minus(w, Minus(x, y))
    assert z._normalize() == Minus(w + y, x)
