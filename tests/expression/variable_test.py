from smoothmath import Point, Partial, Differential, LocatedDifferential
from smoothmath.expression import Variable, Constant
from smoothmath._private.expression.variable import get_variable_name


def test_Variable():
    x = Variable("x")
    y = Variable("y")
    point = Point(y = 3)
    assert y.at(point) == 3
    assert Partial(y, x).at(point) == 0
    assert Partial(y, y).at(point) == 1
    assert Partial(y, x, compute_eagerly = True).at(point) == 0
    assert Partial(y, y, compute_eagerly = True).at(point) == 1
    point = Point(x = 2, y = 3)
    differential = Differential(y)
    assert differential.part_at(x, point) == 0
    assert differential.part_at(y, point) == 1
    located_differential = LocatedDifferential(y, point)
    assert located_differential.part(x) == 0
    assert located_differential.part(y) == 1


def test_Variable_equality():
    assert Variable("x") == Variable("x")
    assert Variable("x") != Variable("y")
    assert Variable("x") != Variable("X")
    assert Variable("x") != Constant(3)


def test_get_variable_name():
    assert get_variable_name(Variable("x")) == "x"
    assert get_variable_name("y") == "y"
