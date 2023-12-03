from pytest import approx
from smoothmath import Point
from smoothmath.expression import Constant, Variable, Square


def test_Square():
    x = Variable("x")
    z = Square(x)
    point = Point({x: 3})
    assert z.evaluate(point) == approx(9)
    assert z.local_partial(point, x) == approx(6)
    assert z.global_partial(x).at(point) == approx(6)
    assert z.local_differential(point).component(x) == approx(6)
    assert z.global_differential().component_at(point, x) == approx(6)


def test_Square_composition():
    x = Variable("x")
    z = Square(Constant(4) * x + Constant(1))
    point = Point({x: 3})
    assert z.evaluate(point) == approx(169)
    assert z.local_partial(point, x) == approx(104)
    assert z.global_partial(x).at(point) == approx(104)
    assert z.local_differential(point).component(x) == approx(104)
    assert z.global_differential().component_at(point, x) == approx(104)
