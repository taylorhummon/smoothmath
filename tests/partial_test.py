from pytest import approx, raises
from smoothmath import DomainError, Point, Partial
from smoothmath.expression import Variable, Constant, Multiply, Logarithm


def test_Partial():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Constant(4) * w + x * y ** 3
    y_partial = Partial(z, y)
    point = Point(w = 7, x = 4, y = 5)
    assert y_partial.at(point) == approx(300)
    assert y_partial.at(point) == approx(300)
    synthetic_y_partial = y_partial.as_expression()
    assert synthetic_y_partial == Multiply(Constant(3), y ** 2, x)


def test_Partial_raises():
    x = Variable("x")
    z = Logarithm(x)
    x_partial = Partial(z, x)
    with raises(DomainError):
        x_partial.at(Point(x = -1))


def test_Partial_equality():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2 + y ** 2
    assert Partial(z, x) == Partial(z, x)
    assert Partial(z, x) != Partial(z, y)


def test_Partial_hashing():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2 + y ** 2
    assert hash(Partial(z, x)) == hash(Partial(z, x))
