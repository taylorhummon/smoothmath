from pytest import approx, raises
from smoothmath import DomainError, Point, Partial
from smoothmath.expression import Variable, Constant, Multiply, Logarithm


# Note: numeric and synthetic partial testing is done in the tests for concrete expressions


def test_Partial():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Constant(4) * w + x * y ** 3
    point = Point(w = 7, x = 4, y = 5)
    partial = Partial(z, y)
    assert partial.at(point) == approx(300)
    partial_expression = partial.as_expression()
    assert partial_expression.at(point) == approx(300)
    assert partial_expression == Multiply(Constant(3), y ** 2, x)
    eager_partial = Partial(z, y, compute_eagerly = True)
    assert eager_partial.at(point) == approx(300)
    eager_partial_expression = eager_partial.as_expression()
    assert eager_partial_expression.at(point) == approx(300)
    assert eager_partial_expression == Multiply(Constant(3), y ** 2, x)


def test_Partial_at_raises():
    x = Variable("x")
    z = Logarithm(x)
    partial = Partial(z, x)
    with raises(DomainError):
        partial.at(Point(x = -1))
    eager_partial = Partial(z, x, compute_eagerly = True)
    with raises(DomainError):
        eager_partial.at(Point(x = -1))


def test_Partial_equality():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2 + y ** 2
    assert Partial(z, x) == Partial(z, x)
    assert Partial(z, x) == Partial(z, x, compute_eagerly = True)
    assert Partial(z, x) != Partial(z, y)


def test_Partial_hashing():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2 + y ** 2
    assert hash(Partial(z, x)) == hash(Partial(z, x))
    assert hash(Partial(z, x)) == hash(Partial(z, x, compute_eagerly = True))
