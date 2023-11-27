from pytest import approx
import math
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Exponential


def test_exponential():
    x = Variable("x")
    z = Exponential(x)
    global_differential = z.compute_global_partials()
    # at x = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, x) == approx(1)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1)
    assert global_differential.partial_at(point, x) == approx(1)
    # at x = 1
    point = Point({x: 1})
    assert z.evaluate(point) == approx(math.e)
    assert z.partial_at(point, x) == approx(math.e)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(math.e)
    assert global_differential.partial_at(point, x) == approx(math.e)
    # at x = -1
    point = Point({x: -1})
    assert z.evaluate(point) == approx(1 / math.e)
    assert z.partial_at(point, x) == approx(1 / math.e)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1 / math.e)
    assert global_differential.partial_at(point, x) == approx(1 / math.e)


def test_Exponential_composition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(6))
    point = Point({x: 3})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, x) == approx(2)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(2)
    assert z.compute_global_partials().partial_at(point, x) == approx(2)


def test_base_two_Exponential():
    x = Variable("x")
    z = Exponential(x, base = 2)
    global_differential = z.compute_global_partials()
    # at x = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(1)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0.693147180559)
    assert z.partial_at(point, x) == approx(0.693147180559)
    assert global_differential.partial_at(point, x) == approx(0.693147180559)
    # at x = 1
    point = Point({x: 1})
    assert z.evaluate(point) == approx(2)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1.386294361119)
    assert z.partial_at(point, x) == approx(1.386294361119)
    assert global_differential.partial_at(point, x) == approx(1.386294361119)
    # at x = -1
    point = Point({x: -1})
    assert z.evaluate(point) == approx(0.5)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0.346573590279)
    assert z.partial_at(point, x) == approx(0.346573590279)
    assert global_differential.partial_at(point, x) == approx(0.346573590279)


def test_base_two_Exponential_composition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(5), base = 2)
    point = Point({x: 3})
    assert z.evaluate(point) == approx(2)
    assert z.partial_at(point, x) == approx(2.77258872223)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(2.77258872223)
    assert z.compute_global_partials().partial_at(point, x) == approx(2.77258872223)
