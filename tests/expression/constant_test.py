from smoothmath import Point
from smoothmath.expression import Constant, Variable


def test_Constant():
    c = Constant(7)
    point = Point({})
    assert c.evaluate(point) == 7
    x = Variable("x")
    point = Point({x: 2})
    assert c.local_partial(point, x) == 0
    assert c.global_partial(x).at(point) == 0
    assert c.local_differential(point).component(x) == 0
    assert c.global_differential().component_at(point, x) == 0


def test_Constant_equality():
    assert Constant(3) == Constant(3)
    assert Constant(3) == Constant(3.0)
    assert Constant(3) != Constant(4)
    assert Constant(3) != Variable("x")
