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
    late_partial = Partial(z, y, compute_early = False)
    assert late_partial.at(point) == approx(300)
    late_partial_expression = late_partial.as_expression()
    assert late_partial_expression.at(point) == approx(300)
    assert late_partial_expression == Multiply(Constant(3), y ** 2, x)
    early_partial = Partial(z, y, compute_early = True)
    assert early_partial.at(point) == approx(300)
    early_partial_expression = early_partial.as_expression()
    assert early_partial_expression.at(point) == approx(300)
    assert early_partial_expression == Multiply(Constant(3), y ** 2, x)


def test_Partial_at_raises():
    x = Variable("x")
    z = Logarithm(x)
    late_partial = Partial(z, x, compute_early = False)
    with raises(DomainError):
        late_partial.at(Point(x = -1))
    early_partial = Partial(z, x, compute_early = True)
    with raises(DomainError):
        early_partial.at(Point(x = -1))


def test_Partial_equality():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2 + y ** 2
    assert Partial(z, x) == Partial(z, x)
    assert Partial(z, x) == Partial(z, x, compute_early = True)
    assert Partial(z, x) != Partial(z, y)


def test_Partial_hashing():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2 + y ** 2
    assert hash(Partial(z, x)) == hash(Partial(z, x))
    assert hash(Partial(z, x)) == hash(Partial(z, x, compute_early = True))
