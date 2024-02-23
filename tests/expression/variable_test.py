from smoothmath import Point, Partial, Differential, LocatedDifferential
from smoothmath.expression import Variable, Constant
from smoothmath._private.expression.variable import get_variable_name


def test_Variable():
    x = Variable("x")
    y = Variable("y")
    point = Point(y = 3)
    assert y.at(point) == 3
    late_differential = Differential(y, compute_early = False)
    assert late_differential.component_at(x, point) == 0
    assert late_differential.component_at(y, point) == 1
    early_differential = Differential(y, compute_early = True)
    assert early_differential.component_at(x, point) == 0
    assert early_differential.component_at(y, point) == 1
    assert Partial(y, x, compute_early = False).at(point) == 0
    assert Partial(y, y, compute_early = False).at(point) == 1
    assert Partial(y, x, compute_early = True).at(point) == 0
    assert Partial(y, y, compute_early = True).at(point) == 1
    point = Point(x = 2, y = 3)
    located_differential = LocatedDifferential(y, point)
    assert located_differential.component(x) == 0
    assert located_differential.component(y) == 1


def test_Variable_equality():
    assert Variable("x") == Variable("x")
    assert Variable("x") != Variable("y")
    assert Variable("x") != Variable("X")
    assert Variable("x") != Constant(3)


def test_get_variable_name():
    assert get_variable_name(Variable("x")) == "x"
    assert get_variable_name("y") == "y"
