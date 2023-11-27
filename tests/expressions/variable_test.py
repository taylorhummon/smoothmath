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
    computed_local_partials = y.compute_local_partials(point)
    assert computed_local_partials.partial_with_respect_to(x) == 0
    assert computed_local_partials.partial_with_respect_to(y) == 1
    synthetic = y.synthetic()
    assert synthetic.partial_at(point, x) == 0
    assert synthetic.partial_at(point, y) == 1
