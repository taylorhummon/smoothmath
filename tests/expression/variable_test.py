from smoothmath import Point, Partial, Differential, LocatedDifferential
from smoothmath.expression import Variable, Constant


def test_Variable():
    x = Variable("x")
    y = Variable("y")
    point = Point(y = 3)
    assert y.evaluate(point) == 3
    assert y.partial_at(x, point) == 0
    assert y.partial_at(y, point) == 1
    assert Partial(y, x).at(point) == 0
    assert Partial(y, y).at(point) == 1
    point = Point(x = 2, y = 3)
    differential = Differential(y)
    assert differential.component_at(x, point) == 0
    assert differential.component_at(y, point) == 1
    located_differential = LocatedDifferential(y, point)
    assert located_differential.component(x) == 0
    assert located_differential.component(y) == 1


def test_Variable_equality():
    assert Variable("x") == Variable("x")
    assert Variable("x") != Variable("y")
    assert Variable("x") != Variable("X")
    assert Variable("x") != Constant(3)
