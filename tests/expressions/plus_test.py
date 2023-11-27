from pytest import approx
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Plus


def test_Plus():
    x = Variable("x")
    y = Variable("y")
    z = Plus(x, y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(5)
    assert z.partial_at(point, x) == approx(1)
    assert z.partial_at(point, y) == approx(1)
    local_differential = z.compute_local_partials(point)
    assert local_differential.partial_with_respect_to(x) == approx(1)
    assert local_differential.partial_with_respect_to(y) == approx(1)
    global_differential = z.compute_global_partials()
    assert global_differential.partial_at(point, x) == approx(1)
    assert global_differential.partial_at(point, y) == approx(1)


def test_Plus_composition():
    x = Variable("x")
    y = Variable("y")
    z = Plus(Constant(5) * x, Constant(4) * y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(22)
    assert z.partial_at(point, x) == approx(5)
    assert z.partial_at(point, y) == approx(4)
    local_differential = z.compute_local_partials(point)
    assert local_differential.partial_with_respect_to(x) == approx(5)
    assert local_differential.partial_with_respect_to(y) == approx(4)
    global_differential = z.compute_global_partials()
    assert global_differential.partial_at(point, x) == approx(5)
    assert global_differential.partial_at(point, y) == approx(4)
