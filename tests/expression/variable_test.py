from smoothmath import Point
from smoothmath.expression import Variable


def test_variable():
    x = Variable("x")
    y = Variable("y")
    point = Point({y: 3})
    assert y.evaluate(point) == 3
    assert y.local_partial(point, x) == 0
    assert y.local_partial(point, y) == 1
    assert y.global_partial(x).at(point) == 0
    assert y.global_partial(y).at(point) == 1
    point = Point({x: 2, y: 3})
    local_differential = y.local_differential(point)
    assert local_differential.component(x) == 0
    assert local_differential.component(y) == 1
    global_differential = y.global_differential()
    assert global_differential.component_at(point, x) == 0
    assert global_differential.component_at(point, y) == 1
