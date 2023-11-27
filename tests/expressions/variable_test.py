from smoothmath.point import Point
from smoothmath.expressions import Variable


def test_variable():
    x = Variable("x")
    y = Variable("y")
    point = Point({y: 3})
    assert y.evaluate(point) == 3
    assert y.partial_at(point, x) == 0
    assert y.partial_at(point, y) == 1
    point = Point({x: 2, y: 3})
    local_differential = y.compute_local_partials(point)
    assert local_differential.partial_with_respect_to(x) == 0
    assert local_differential.partial_with_respect_to(y) == 1
    global_differential = y.compute_global_partials()
    assert global_differential.partial_at(point, x) == 0
    assert global_differential.partial_at(point, y) == 1
