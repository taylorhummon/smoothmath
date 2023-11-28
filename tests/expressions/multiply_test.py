from pytest import approx
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Multiply


def test_Multiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(6)
    assert z.local_partial(point, x) == approx(3)
    assert z.local_partial(point, y) == approx(2)
    assert z.global_partial(x).at(point) == approx(3)
    assert z.global_partial(y).at(point) == approx(2)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(3)
    assert local_differential.component(y) == approx(2)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(3)
    assert global_differential.component_at(point, y) == approx(2)


def test_Multiply_composition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    point = Point({x: 2, y: 4})
    assert z.evaluate(point) == approx(30)
    assert z.local_partial(point, x) == approx(15)
    assert z.local_partial(point, y) == approx(10)
    assert z.global_partial(x).at(point) == approx(15)
    assert z.global_partial(y).at(point) == approx(10)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(15)
    assert local_differential.component(y) == approx(10)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(15)
    assert global_differential.component_at(point, y) == approx(10)


def test_Multiply_by_zero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(0)
    assert z.global_partial(x).at(point) == approx(0)
    assert z.local_differential(point).component(x) == approx(0)
    assert z.global_differential().component_at(point, x) == approx(0)


def test_Multiply_by_one():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(point, x) == approx(1)
    assert z.global_partial(x).at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert z.global_differential().component_at(point, x) == approx(1)
