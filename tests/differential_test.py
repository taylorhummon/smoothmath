from pytest import approx, raises
from smoothmath import DomainError, Point, Partial, Differential, LocatedDifferential
from smoothmath.expression import Variable, Constant, Logarithm


# Note: intensive testing of numeric and synthetic partials is done in the tests for concrete expressions


def test_Differential():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Constant(4) * w + x * y ** 3
    point = Point(w = 7, x = 4, y = 5)
    differential = Differential(z)
    # part_at() method
    assert differential.part_at(w, point) == approx(4)
    assert differential.part_at(x, point) == approx(125)
    assert differential.part_at(y, point) == approx(300)
    assert differential.part_at("w", point) == approx(4)
    assert differential.part_at("x", point) == approx(125)
    assert differential.part_at("y", point) == approx(300)
    # part() method
    assert differential.part(w) == Partial(z, w)
    assert differential.part(x) == Partial(z, x)
    assert differential.part(y) == Partial(z, y)
    assert differential.part("w") == Partial(z, w)
    assert differential.part("x") == Partial(z, x)
    assert differential.part("y") == Partial(z, y)
    # at() method
    assert differential.at(point) == LocatedDifferential(z, point)
    # eagerly computed differential
    eager_differential = Differential(z, compute_eagerly = True)
    # part_at() method
    assert eager_differential.part_at(w, point) == approx(4)
    assert eager_differential.part_at(x, point) == approx(125)
    assert eager_differential.part_at(y, point) == approx(300)
    assert eager_differential.part_at("w", point) == approx(4)
    assert eager_differential.part_at("x", point) == approx(125)
    assert eager_differential.part_at("y", point) == approx(300)
    # part() method
    assert eager_differential.part(w) == Partial(z, w)
    assert eager_differential.part(x) == Partial(z, x)
    assert eager_differential.part(y) == Partial(z, y)
    assert eager_differential.part("w") == Partial(z, w)
    assert eager_differential.part("x") == Partial(z, x)
    assert eager_differential.part("y") == Partial(z, y)
    # at() method
    assert eager_differential.at(point) == LocatedDifferential(z, point)


def test_Differential_raises():
    x = Variable("x")
    z = Logarithm(x)
    point = Point(x = -1)
    differential = Differential(z)
    with raises(DomainError):
        differential.part_at(x, point)
    x_partial = differential.part(x)
    with raises(DomainError):
        x_partial.at(point)
    with raises(DomainError):
        differential.at(point)
    eager_differential = Differential(z)
    with raises(DomainError):
        eager_differential.part_at(x, point)
    x_partial = eager_differential.part(x)
    with raises(DomainError):
        x_partial.at(point)
    with raises(DomainError):
        eager_differential.at(point)


def test_LocatedDifferential_equality():
    x = Variable("x")
    y = Variable("y")
    assert Differential(x * y ** 3) == Differential(x * y ** 3)
    assert Differential(x * y ** 3) == Differential(x * y ** 3, compute_eagerly = True)
    assert Differential(x * y ** 3) != Differential(y * x ** 3)


def test_LocatedDifferential_hashing():
    x = Variable("x")
    y = Variable("y")
    z = x * y ** 3
    assert hash(Differential(z)) == hash(Differential(z))
    assert hash(Differential(z)) == hash(Differential(z, compute_eagerly = True))
