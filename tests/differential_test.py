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
    late_differential = Differential(z, compute_early = False)
    assert late_differential.component_at(w, point) == approx(4)
    assert late_differential.component_at(x, point) == approx(125)
    assert late_differential.component_at(y, point) == approx(300)
    assert late_differential.component_at("w", point) == approx(4)
    assert late_differential.component_at("x", point) == approx(125)
    assert late_differential.component_at("y", point) == approx(300)
    assert late_differential.component(w) == Partial(z, w)
    assert late_differential.component(x) == Partial(z, x)
    assert late_differential.component(y) == Partial(z, y)
    assert late_differential.component("w") == Partial(z, w)
    assert late_differential.component("x") == Partial(z, x)
    assert late_differential.component("y") == Partial(z, y)
    assert late_differential.at(point) == LocatedDifferential(z, point)
    early_differential = Differential(z, compute_early = True)
    assert early_differential.component_at(w, point) == approx(4)
    assert early_differential.component_at(x, point) == approx(125)
    assert early_differential.component_at(y, point) == approx(300)
    assert early_differential.component_at("w", point) == approx(4)
    assert early_differential.component_at("x", point) == approx(125)
    assert early_differential.component_at("y", point) == approx(300)
    assert early_differential.component(w) == Partial(z, w)
    assert early_differential.component(x) == Partial(z, x)
    assert early_differential.component(y) == Partial(z, y)
    assert early_differential.component("w") == Partial(z, w)
    assert early_differential.component("x") == Partial(z, x)
    assert early_differential.component("y") == Partial(z, y)
    assert early_differential.at(point) == LocatedDifferential(z, point)


def test_Differential_raises():
    x = Variable("x")
    z = Logarithm(x)
    point = Point(x = -1)
    late_differential = Differential(z, compute_early = False)
    with raises(DomainError):
        late_differential.component_at(x, point)
    x_partial = late_differential.component(x)
    with raises(DomainError):
        x_partial.at(point)
    with raises(DomainError):
        late_differential.at(point)
    early_differential = Differential(z, compute_early = True)
    with raises(DomainError):
        early_differential.component_at(x, point)
    x_partial = early_differential.component(x)
    with raises(DomainError):
        x_partial.at(point)
    with raises(DomainError):
        early_differential.at(point)


def test_LocatedDifferential_equality():
    x = Variable("x")
    y = Variable("y")
    assert Differential(x * y ** 3) == Differential(x * y ** 3)
    assert Differential(x * y ** 3) == Differential(x * y ** 3, compute_early = True)
    assert Differential(x * y ** 3) != Differential(y * x ** 3)


def test_LocatedDifferential_hashing():
    x = Variable("x")
    y = Variable("y")
    z = x * y ** 3
    assert hash(Differential(z)) == hash(Differential(z))
    assert hash(Differential(z)) == hash(Differential(z, compute_early = True))
