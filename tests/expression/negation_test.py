from pytest import approx
from smoothmath import Point
from smoothmath.expression import Constant, Variable, Negation


def test_Negation():
    x = Variable("x")
    z = Negation(x)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(-2)
    assert z.local_partial(point, x) == approx(-1)
    assert z.global_partial(x).at(point) == approx(-1)
    assert z.local_differential(point).component(x) == approx(-1)
    assert z.global_differential().component_at(point, x) == approx(-1)


def test_Negation_composition():
    x = Variable("x")
    z = Negation(Constant(2) * x + Constant(1))
    point = Point({x: 3})
    assert z.evaluate(point) == approx(-7)
    assert z.local_partial(point, x) == approx(-2)
    assert z.global_partial(x).at(point) == approx(-2)
    assert z.local_differential(point).component(x) == approx(-2)
    assert z.global_differential().component_at(point, x) == approx(-2)


def test_reduce_negation_of_negation_of_u():
    u = Variable("u")
    z = Negation(Negation(u))
    assert z._reduce_negation_of_negation_of_u() == u
