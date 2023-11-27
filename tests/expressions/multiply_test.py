from pytest import approx
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Multiply


def test_Multiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(6)
    assert z.partial_at(point, x) == approx(3)
    assert z.partial_at(point, y) == approx(2)
    local_differential = z.compute_local_partials(point)
    assert local_differential.partial_with_respect_to(x) == approx(3)
    assert local_differential.partial_with_respect_to(y) == approx(2)
    global_differential = z.compute_global_partials()
    assert global_differential.partial_at(point, x) == approx(3)
    assert global_differential.partial_at(point, y) == approx(2)


def test_Multiply_composition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(20)
    assert z.partial_at(point, x) == approx(10)
    assert z.partial_at(point, y) == approx(10)
    local_differential = z.compute_local_partials(point)
    assert local_differential.partial_with_respect_to(x) == approx(10)
    assert local_differential.partial_with_respect_to(y) == approx(10)
    global_differential = z.compute_global_partials()
    assert global_differential.partial_at(point, x) == approx(10)
    assert global_differential.partial_at(point, y) == approx(10)


def test_Multiply_by_zero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, x) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0)
    assert z.compute_global_partials().partial_at(point, x) == approx(0)


def test_Multiply_by_one():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(2)
    assert z.partial_at(point, x) == approx(1)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1)
    assert z.compute_global_partials().partial_at(point, x) == approx(1)
