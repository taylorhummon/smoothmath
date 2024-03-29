from smoothmath import Point, Partial, Differential, LocatedDifferential
from smoothmath.expression import Variable, Constant


def test_Constant():
    c = Constant(7)
    point = Point()
    assert c.at(point) == 7
    x = Variable("x")
    point = Point(x = 2)
    assert Differential(c, compute_early = False).component_at(x, point) == 0
    assert Differential(c, compute_early = True).component_at(x, point) == 0
    assert Partial(c, x, compute_early = False).at(point) == 0
    assert Partial(c, x, compute_early = True).at(point) == 0
    assert LocatedDifferential(c, point).component(x) == 0


def test_Constant_equality():
    assert Constant(3) == Constant(3)
    assert Constant(3) == Constant(3.0)
    assert Constant(3) != Constant(4)
    assert Constant(3) != Variable("x")
