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
    all_partials = y.all_partials_at(point)
    assert all_partials.partial_with_respect_to(x) == 0
    assert all_partials.partial_with_respect_to(y) == 1
    synthetic = y.synthetic()
    assert synthetic.partial_at(point, x) == 0
    assert synthetic.partial_at(point, y) == 1
