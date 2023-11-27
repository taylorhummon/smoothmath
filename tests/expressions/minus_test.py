from pytest import approx
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Minus


def test_Minus():
    x = Variable("x")
    y = Variable("y")
    z = Minus(x, y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(-1)
    assert z.partial_at(point, x) == approx(1)
    assert z.partial_at(point, y) == approx(-1)
    computed_local_partials = z.compute_local_partials(point)
    assert computed_local_partials.partial_with_respect_to(x) == approx(1)
    assert computed_local_partials.partial_with_respect_to(y) == approx(-1)
    computed_global_partials = z.compute_global_partials()
    assert computed_global_partials.partial_at(point, x) == approx(1)
    assert computed_global_partials.partial_at(point, y) == approx(-1)


def test_Minus_composition():
    x = Variable("x")
    y = Variable("y")
    z = Minus(Constant(5) * x, Constant(4) * y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(-2)
    assert z.partial_at(point, x) == approx(5)
    assert z.partial_at(point, y) == approx(-4)
    computed_local_partials = z.compute_local_partials(point)
    assert computed_local_partials.partial_with_respect_to(x) == approx(5)
    assert computed_local_partials.partial_with_respect_to(y) == approx(-4)
    computed_global_partials = z.compute_global_partials()
    assert computed_global_partials.partial_at(point, x) == approx(5)
    assert computed_global_partials.partial_at(point, y) == approx(-4)
