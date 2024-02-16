from pytest import approx, raises
from smoothmath import DomainError, Point, Partial
from smoothmath.expression import Variable, Constant, Multiply, Logarithm


# Note: intensive testing of partials is done in the tests for concrete expressions


def test_Partial():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Constant(4) * w + x * y ** 3
    point = Point(w = 7, x = 4, y = 5)
    partial = Partial(z, y)
    assert partial.at(point) == approx(300)
    assert partial.as_expression() == Multiply(Constant(3), y ** 2, x)
    eager_partial = Partial(z, y, compute_eagerly = True)
    assert eager_partial.at(point) == approx(300)
    assert eager_partial.as_expression() == Multiply(Constant(3), y ** 2, x)


def test_Partial_at_raises():
    x = Variable("x")
    z = Logarithm(x)
    partial = Partial(z, x)
    with raises(DomainError):
        partial.at(Point(x = -1))


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
