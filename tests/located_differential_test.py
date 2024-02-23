from pytest import approx, raises
from smoothmath import DomainError, Point, LocatedDifferential
from smoothmath.expression import Variable, Constant, Logarithm


# Note: numeric partials testing is done in the tests for concrete expressions


def test_LocatedDifferential():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Constant(4) * w + x * y ** 3
    point = Point(w = 7, x = 4, y = 5)
    located_differential = LocatedDifferential(z, point)
    assert located_differential.component(w) == approx(4)
    assert located_differential.component(x) == approx(125)
    assert located_differential.component(y) == approx(300)
    assert located_differential.component("w") == approx(4)
    assert located_differential.component("x") == approx(125)
    assert located_differential.component("y") == approx(300)


def test_LocatedDifferential_raises():
    x = Variable("x")
    y = Variable("y")
    z = Logarithm(x) * y
    point = Point(x = -1, y = 1)
    with raises(DomainError):
        LocatedDifferential(z, point)


def test_LocatedDifferential_equality():
    x = Variable("x")
    y = Variable("y")
    point_a = Point(x = 1, y = 1)
    assert LocatedDifferential(x, point_a) == LocatedDifferential(x, point_a)
    assert LocatedDifferential(x, point_a) != LocatedDifferential(y, point_a)
    point_b = Point(x = 1, y = 2)
    assert LocatedDifferential(x, point_a) != LocatedDifferential(x, point_b)


def test_LocatedDifferential_hashing():
    x = Variable("x")
    y = Variable("y")
    z = x * y ** 3
    point = Point(x = 1, y = 2)
    assert hash(LocatedDifferential(z, point)) == hash(LocatedDifferential(z, point))
