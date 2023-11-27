from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Reciprocal


def test_Reciprocal():
    x = Variable("x")
    z = Reciprocal(x)
    synthetic = z.synthetic()
    # at x = 2
    point = Point({x: 2})
    assert z.evaluate(point) == approx(0.5)
    assert z.partial_at(point, x) == approx(-0.25)
    assert z.all_partials_at(point).partial_with_respect_to(x) == approx(-0.25)
    assert synthetic.partial_at(point, x) == approx(-0.25)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.all_partials_at(point)
    with raises(DomainError):
        synthetic.partial_at(point, x)
    # at x = -1
    point = Point({x: -1})
    assert z.evaluate(point) == approx(-1)
    assert z.partial_at(point, x) == approx(-1)
    assert z.all_partials_at(point).partial_with_respect_to(x) == approx(-1)
    assert synthetic.partial_at(point, x) == approx(-1)


def test_Reciprocal_composition():
    x = Variable("x")
    z = Reciprocal(Constant(2) * x - Constant(4))
    point = Point({x: 3})
    assert z.evaluate(point) == approx(0.5)
    assert z.partial_at(point, x) == approx(-0.5)
    assert z.all_partials_at(point).partial_with_respect_to(x) == approx(-0.5)
    assert z.synthetic().partial_at(point, x) == approx(-0.5)
