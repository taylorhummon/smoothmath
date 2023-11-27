from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, SquareRoot


def test_SquareRoot():
    x = Variable("x")
    z = SquareRoot(x)
    global_differential = z.compute_global_partials()
    # at x = 4
    point = Point({x: 4})
    assert z.evaluate(point) == approx(2)
    assert z.partial_at(point, x) == approx(0.25)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0.25)
    assert global_differential.partial_at(point, x) == approx(0.25)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        global_differential.partial_at(point, x)
    # at x = -1
    point = Point({x: -1})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        global_differential.partial_at(point, x)


def test_SquareRoot_composition():
    x = Variable("x")
    z = SquareRoot(Constant(2) * x + Constant(7))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(3)
    assert z.partial_at(point, x) == approx(1 / 3)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1 / 3)
    assert z.compute_global_partials().partial_at(point, x) == approx(1 / 3)
