from smoothmath import Point, GlobalDifferential, LocalDifferential, GlobalPartial
from smoothmath.expression import Variable, Constant


def test_Variable():
    x = Variable("x")
    y = Variable("y")
    point = Point(y = 3)
    assert y.evaluate(point) == 3
    assert y.partial_at(x, point) == 0
    assert y.partial_at(y, point) == 1
    assert GlobalPartial(y, x).at(point) == 0
    assert GlobalPartial(y, y).at(point) == 1
    point = Point(x = 2, y = 3)
    local_differential = LocalDifferential(y, point)
    assert local_differential.component(x) == 0
    assert local_differential.component(y) == 1
    global_differential = GlobalDifferential(y)
    assert global_differential.component_at(x, point) == 0
    assert global_differential.component_at(y, point) == 1


def test_Variable_equality():
    assert Variable("x") == Variable("x")
    assert Variable("x") != Variable("y")
    assert Variable("x") != Variable("X")
    assert Variable("x") != Constant(3)
