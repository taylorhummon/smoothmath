from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Reciprocal


def test_Reciprocal():
    x = Variable("x")
    z = Reciprocal(x)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 2
    point = Point({x: 2})
    assert z.evaluate(point) == approx(0.5)
    assert z.local_partial(point, x) == approx(-0.25)
    assert global_x_partial.at(point) == approx(-0.25)
    assert z.local_differential(point).component(x) == approx(-0.25)
    assert global_differential.component_at(point, x) == approx(-0.25)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    # at x = -1
    point = Point({x: -1})
    assert z.evaluate(point) == approx(-1)
    assert z.local_partial(point, x) == approx(-1)
    assert global_x_partial.at(point) == approx(-1)
    assert z.local_differential(point).component(x) == approx(-1)
    assert global_differential.component_at(point, x) == approx(-1)


def test_Reciprocal_composition():
    x = Variable("x")
    z = Reciprocal(Constant(2) * x - Constant(4))
    point = Point({x: 3})
    assert z.evaluate(point) == approx(0.5)
    assert z.local_partial(point, x) == approx(-0.5)
    assert z.global_partial(x).at(point) == approx(-0.5)
    assert z.local_differential(point).component(x) == approx(-0.5)
    assert z.global_differential().component_at(point, x) == approx(-0.5)
