from pytest import approx
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Negation


def test_Negation():
    x = Variable("x")
    z = Negation(x)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(-2)
    assert z.partial_at(point, x) == approx(-1)
    assert z.all_partials_at(point).partial_with_respect_to(x) == approx(-1)
    assert z.synthetic().partial_at(point, x) == approx(-1)


def test_Negation_composition():
    x = Variable("x")
    z = Negation(Constant(2) * x + Constant(1))
    point = Point({x: 3})
    assert z.evaluate(point) == approx(-7)
    assert z.partial_at(point, x) == approx(-2)
    assert z.all_partials_at(point).partial_with_respect_to(x) == approx(-2)
    assert z.synthetic().partial_at(point, x) == approx(-2)
