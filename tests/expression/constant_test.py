from smoothmath import Point, Partial, Differential, LocatedDifferential
from smoothmath.expression import Variable, Constant


def test_Constant():
    c = Constant(7)
    point = Point()
    assert c.at(point) == 7
    x = Variable("x")
    point = Point(x = 2)
    assert Partial(c, x).at(point) == 0
    assert Partial(c, x, compute_eagerly = True).at(point) == 0
    assert Differential(c).part_at(x, point) == 0
    assert LocatedDifferential(c, point).part(x) == 0


def test_Constant_equality():
    assert Constant(3) == Constant(3)
    assert Constant(3) == Constant(3.0)
    assert Constant(3) != Constant(4)
    assert Constant(3) != Variable("x")
