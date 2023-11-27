from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable


def test_Constant():
    c = Constant(7)
    point = Point({})
    assert c.evaluate(point) == 7
    x = Variable("x")
    point = Point({x: 2})
    assert c.partial_at(point, x) == 0
    assert c.compute_local_partials(point).partial_with_respect_to(x) == 0
    assert c.compute_global_partials().partial_at(point, x) == 0
