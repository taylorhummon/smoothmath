from pytest import approx, raises
from smoothmath import DomainError, Point, GlobalPartial, LocalDifferential, GlobalDifferential
from smoothmath.expression import Variable, Constant, Logarithm


def test_GlobalDifferential():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Constant(4) * w + x * y ** 3
    global_differential = GlobalDifferential(z)
    point = Point(w = 7, x = 4, y = 5)
    # component_at() method
    assert global_differential.component_at(w, point) == approx(4)
    assert global_differential.component_at(x, point) == approx(125)
    assert global_differential.component_at(y, point) == approx(300)
    assert global_differential.component_at("w", point) == approx(4)
    assert global_differential.component_at("x", point) == approx(125)
    assert global_differential.component_at("y", point) == approx(300)
    # component() method
    assert global_differential.component(w) == GlobalPartial(z, w)
    assert global_differential.component(x) == GlobalPartial(z, x)
    assert global_differential.component(y) == GlobalPartial(z, y)
    assert global_differential.component("w") == GlobalPartial(z, w)
    assert global_differential.component("x") == GlobalPartial(z, x)
    assert global_differential.component("y") == GlobalPartial(z, y)
    # at() method
    assert global_differential.at(point) == LocalDifferential(z, point)


def test_GlobalDifferential_raises():
    x = Variable("x")
    z = Logarithm(x)
    global_differential = GlobalDifferential(z)
    point = Point(x = -1)
    with raises(DomainError):
        global_differential.component_at(x, point)
    global_x_partial = global_differential.component(x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        global_differential.at(point)


def test_LocalDifferential_equality():
    x = Variable("x")
    y = Variable("y")
    assert GlobalDifferential(x * y ** 3) == GlobalDifferential(x * y ** 3)
    assert GlobalDifferential(x * y ** 3) != GlobalDifferential(y * x ** 3)


def test_LocalDifferential_hashing():
    x = Variable("x")
    y = Variable("y")
    z = x * y ** 3
    assert hash(GlobalDifferential(z)) == hash(GlobalDifferential(z))
