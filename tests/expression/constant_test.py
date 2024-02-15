from smoothmath import Point, GlobalDifferential, LocalDifferential, Partial
from smoothmath.expression import Variable, Constant


def test_Constant():
    c = Constant(7)
    point = Point()
    assert c.evaluate(point) == 7
    x = Variable("x")
    point = Point(x = 2)
    assert c.partial_at(x, point) == 0
    assert Partial(c, x).at(point) == 0
    assert LocalDifferential(c, point).component(x) == 0
    assert GlobalDifferential(c).component_at(x, point) == 0


def test_Constant_equality():
    assert Constant(3) == Constant(3)
    assert Constant(3) == Constant(3.0)
    assert Constant(3) != Constant(4)
    assert Constant(3) != Variable("x")
