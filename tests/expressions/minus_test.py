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
    both_partials = z.all_partials_at(point)
    assert both_partials.partial_with_respect_to(x) == approx(1)
    assert both_partials.partial_with_respect_to(y) == approx(-1)
    synthetic = z.synthetic()
    assert synthetic.partial_at(point, x) == approx(1)
    assert synthetic.partial_at(point, y) == approx(-1)


def test_Minus_composition():
    x = Variable("x")
    y = Variable("y")
    z = Minus(Constant(5) * x, Constant(4) * y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(-2)
    assert z.partial_at(point, x) == approx(5)
    assert z.partial_at(point, y) == approx(-4)
    both_partials = z.all_partials_at(point)
    assert both_partials.partial_with_respect_to(x) == approx(5)
    assert both_partials.partial_with_respect_to(y) == approx(-4)
    synthetic = z.synthetic()
    assert synthetic.partial_at(point, x) == approx(5)
    assert synthetic.partial_at(point, y) == approx(-4)
