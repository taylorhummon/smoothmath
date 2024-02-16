from pytest import approx, raises
from smoothmath import DomainError, Point, Partial, Differential, LocatedDifferential
from smoothmath.expression import Variable, Constant, Logarithm


def test_Differential():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Constant(4) * w + x * y ** 3
    differential = Differential(z)
    point = Point(w = 7, x = 4, y = 5)
    # component_at() method
    assert differential.component_at(w, point) == approx(4)
    assert differential.component_at(x, point) == approx(125)
    assert differential.component_at(y, point) == approx(300)
    assert differential.component_at("w", point) == approx(4)
    assert differential.component_at("x", point) == approx(125)
    assert differential.component_at("y", point) == approx(300)
    # component() method
    assert differential.component(w) == Partial(z, w)
    assert differential.component(x) == Partial(z, x)
    assert differential.component(y) == Partial(z, y)
    assert differential.component("w") == Partial(z, w)
    assert differential.component("x") == Partial(z, x)
    assert differential.component("y") == Partial(z, y)
    # at() method
    assert differential.at(point) == LocatedDifferential(z, point)


def test_Differential_raises():
    x = Variable("x")
    z = Logarithm(x)
    differential = Differential(z)
    point = Point(x = -1)
    with raises(DomainError):
        differential.component_at(x, point)
    x_partial = differential.component(x)
    with raises(DomainError):
        x_partial.at(point)
    with raises(DomainError):
        differential.at(point)


def test_LocatedDifferential_equality():
    x = Variable("x")
    y = Variable("y")
    assert Differential(x * y ** 3) == Differential(x * y ** 3)
    assert Differential(x * y ** 3) != Differential(y * x ** 3)


def test_LocatedDifferential_hashing():
    x = Variable("x")
    y = Variable("y")
    z = x * y ** 3
    assert hash(Differential(z)) == hash(Differential(z))
