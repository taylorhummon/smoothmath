from pytest import approx
from smoothmath import Point, LocalDifferential
from smoothmath.expression import Variable, Constant


def test_LocalDifferential():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Constant(4) * w + x * y ** 3
    point = Point(w = 7, x = 4, y = 5)
    local_differential = LocalDifferential(z, point)
    assert local_differential.component(w) == approx(4)
    assert local_differential.component(x) == approx(125)
    assert local_differential.component(y) == approx(300)
    assert local_differential.component("w") == approx(4)
    assert local_differential.component("x") == approx(125)
    assert local_differential.component("y") == approx(300)


def test_LocalDifferential_equality():
    x = Variable("x")
    y = Variable("y")
    point_a = Point(x = 1, y = 1)
    assert LocalDifferential(x, point_a) == LocalDifferential(x, point_a)
    assert LocalDifferential(x, point_a) != LocalDifferential(y, point_a)
    point_b = Point(x = 1, y = 2)
    assert LocalDifferential(x, point_a) != LocalDifferential(x, point_b)


def test_LocalDifferential_hashing():
    x = Variable("x")
    y = Variable("y")
    z = x * y ** 3
    point = Point(x = 1, y = 2)
    assert hash(LocalDifferential(z, point)) == hash(LocalDifferential(z, point))
