from pytest import approx
from smoothmath import Point
from smoothmath.expression import Constant, Variable, Minus


def test_Minus():
    x = Variable("x")
    y = Variable("y")
    z = Minus(x, y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(-1)
    assert z.local_partial(point, x) == approx(1)
    assert z.local_partial(point, y) == approx(-1)
    assert z.global_partial(x).at(point) == approx(1)
    assert z.global_partial(y).at(point) == approx(-1)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(1)
    assert local_differential.component(y) == approx(-1)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(1)
    assert global_differential.component_at(point, y) == approx(-1)


def test_Minus_composition():
    x = Variable("x")
    y = Variable("y")
    z = Minus(Constant(5) * x, Constant(4) * y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(-2)
    assert z.local_partial(point, x) == approx(5)
    assert z.local_partial(point, y) == approx(-4)
    assert z.global_partial(x).at(point) == approx(5)
    assert z.global_partial(y).at(point) == approx(-4)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(5)
    assert local_differential.component(y) == approx(-4)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(5)
    assert global_differential.component_at(point, y) == approx(-4)