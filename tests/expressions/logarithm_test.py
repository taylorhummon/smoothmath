from pytest import approx, raises
import math
from smoothmath.errors import DomainError
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Logarithm


def test_Logarithm():
    x = Variable("x")
    z = Logarithm(x)
    computed_global_partials = z.compute_global_partials()
    # at x = 1
    point = Point({x: 1})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, x) == approx(1)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1)
    assert computed_global_partials.partial_at(point, x) == approx(1)
    # at x = e
    point = Point({x: math.e})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, x) == approx(1 / math.e)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1 / math.e)
    assert computed_global_partials.partial_at(point, x) == approx(1 / math.e)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)
    # at x = -1
    point = Point({x: -1})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)


def test_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(3))
    point = Point({x: 2})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, x) == approx(2)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(2)
    assert z.compute_global_partials().partial_at(point, x) == approx(2)


def test_base_two_Logarithm():
    x = Variable("x")
    z = Logarithm(x, base = 2)
    computed_global_partials = z.compute_global_partials()
    # at x = 1
    point = Point({x: 1})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, x) == approx(1.442695040888)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1.442695040888)
    assert computed_global_partials.partial_at(point, x) == approx(1.442695040888)
    # at x = 2
    point = Point({x: 2})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, x) == approx(0.721347520444)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0.721347520444)
    assert computed_global_partials.partial_at(point, x) == approx(0.721347520444)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)
    # at x = -1
    point = Point({x: -1})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)


def test_base_two_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(6), base = 2)
    point = Point({x: 7})
    assert z.evaluate(point) == approx(3)
    assert z.partial_at(point, x) == approx(0.3606737602222)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0.3606737602222)
    assert z.compute_global_partials().partial_at(point, x) == approx(0.3606737602222)
