from pytest import approx
import math
from smoothmath import Point
from smoothmath.expression import Constant, Variable, Exponential


def test_exponential():
    x = Variable("x")
    z = Exponential(x)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, x) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)
    # at x = 1
    point = Point({x: 1})
    assert z.evaluate(point) == approx(math.e)
    assert z.local_partial(point, x) == approx(math.e)
    assert global_x_partial.at(point) == approx(math.e)
    assert z.local_differential(point).component(x) == approx(math.e)
    assert global_differential.component_at(point, x) == approx(math.e)
    # at x = -1
    point = Point({x: -1})
    assert z.evaluate(point) == approx(1 / math.e)
    assert z.local_partial(point, x) == approx(1 / math.e)
    assert global_x_partial.at(point) == approx(1 / math.e)
    assert z.local_differential(point).component(x) == approx(1 / math.e)
    assert global_differential.component_at(point, x) == approx(1 / math.e)


def test_Exponential_composition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(6))
    point = Point({x: 3})
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, x) == approx(2)
    assert z.global_partial(x).at(point) == approx(2)
    assert z.local_differential(point).component(x) == approx(2)
    assert z.global_differential().component_at(point, x) == approx(2)


def test_base_two_Exponential():
    x = Variable("x")
    z = Exponential(x, base = 2)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(0.693147180559)
    assert global_x_partial.at(point) == approx(0.693147180559)
    assert z.local_partial(point, x) == approx(0.693147180559)
    assert global_differential.component_at(point, x) == approx(0.693147180559)
    # at x = 1
    point = Point({x: 1})
    assert z.evaluate(point) == approx(2)
    assert z.local_differential(point).component(x) == approx(1.386294361119)
    assert global_x_partial.at(point) == approx(1.386294361119)
    assert z.local_partial(point, x) == approx(1.386294361119)
    assert global_differential.component_at(point, x) == approx(1.386294361119)
    # at x = -1
    point = Point({x: -1})
    assert z.evaluate(point) == approx(0.5)
    assert z.local_differential(point).component(x) == approx(0.346573590279)
    assert global_x_partial.at(point) == approx(0.346573590279)
    assert z.local_partial(point, x) == approx(0.346573590279)
    assert global_differential.component_at(point, x) == approx(0.346573590279)


def test_base_two_Exponential_composition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(5), base = 2)
    point = Point({x: 3})
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(point, x) == approx(2.77258872223)
    assert z.global_partial(x).at(point) == approx(2.77258872223)
    assert z.local_differential(point).component(x) == approx(2.77258872223)
    assert z.global_differential().component_at(point, x) == approx(2.77258872223)
