from pytest import approx
from smoothmath import Point
from smoothmath.expression import (
    Variable, Constant, Negation, Reciprocal, NthPower, NthRoot, Exponential
)


def test_NthPower_with_n_equal_two():
    x = Variable("x")
    z = NthPower(x, n = 2)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 3
    point = Point(x = 3)
    assert z.evaluate(point) == approx(9)
    assert z.local_partial(x, point) == approx(6)
    assert global_x_partial.at(point) == approx(6)
    assert z.local_differential(point).component(x) == approx(6)
    assert global_differential.component_at(x, point) == approx(6)
    # at x = 0
    point = Point(x = 0)
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(x, point) == approx(0)
    assert global_x_partial.at(point) == approx(0)
    assert z.local_differential(point).component(x) == approx(0)
    assert global_differential.component_at(x, point) == approx(0)
    # at x = -5
    point = Point(x = -5)
    assert z.evaluate(point) == approx(25)
    assert z.local_partial(x, point) == approx(-10)
    assert global_x_partial.at(point) == approx(-10)
    assert z.local_differential(point).component(x) == approx(-10)
    assert global_differential.component_at(x, point) == approx(-10)


def test_NthPower_with_n_equal_two_composition():
    x = Variable("x")
    z = NthPower(Constant(3) * x - Constant(1), n = 2)
    point = Point(x = 1)
    assert z.evaluate(point) == approx(4)
    assert z.local_partial(x, point) == approx(12)
    assert z.global_partial(x).at(point) == approx(12)
    assert z.local_differential(point).component(x) == approx(12)
    assert z.global_differential().component_at(x, point) == approx(12)


def test_NthPower_with_n_equal_one():
    x = Variable("x")
    z = NthPower(x, n = 1)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 3
    point = Point(x = 3)
    assert z.evaluate(point) == approx(3)
    assert z.local_partial(x, point) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(x, point) == approx(1)
    # at x = 0
    point = Point(x = 0)
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(x, point) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(x, point) == approx(1)
    # at x = -5
    point = Point(x = -5)
    assert z.evaluate(point) == approx(-5)
    assert z.local_partial(x, point) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(x, point) == approx(1)


def test_NthPower_with_n_equal_one_composition():
    x = Variable("x")
    z = NthPower(Constant(3) * x - Constant(1), n = 1)
    point = Point(x = 1)
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(x, point) == approx(3)
    assert z.global_partial(x).at(point) == approx(3)
    assert z.local_differential(point).component(x) == approx(3)
    assert z.global_differential().component_at(x, point) == approx(3)


def test_NthPower_normalization():
    x = Variable("x")
    z = NthPower(x, n = 1)
    assert z._normalize() == x
    z = NthPower(x, n = 2)
    assert z._normalize() == NthPower(x, n = 2)
    z = NthPower(NthPower(x, n = 3), n = 2)
    assert z._normalize() == NthPower(x, n = 6)
    z = NthPower(NthRoot(x, n = 2), n = 2)
    assert z._normalize() == x
    z = NthPower(NthRoot(x, n = 2), n = 6)
    assert z._normalize() == NthPower(x, n = 3)
    z = NthPower(NthRoot(x, n = 6), n = 2)
    assert z._normalize() == NthRoot(x, n = 3)
    z = NthPower(NthRoot(x, n = 6), n = 4)
    assert z._normalize() == NthPower(NthRoot(x, n = 3), n = 2)
    z = NthPower(NthRoot(x, n = 4), n = 6)
    assert z._normalize() == NthPower(NthRoot(x, n = 2), n = 3)
    z = NthPower(Negation(x), n = 2)
    assert z._normalize() == NthPower(x, n = 2)
    z = NthPower(Negation(x), n = 3)
    assert z._normalize() == Negation(NthPower(x, n = 3))
    z = NthPower(Reciprocal(x), n = 2)
    assert z._normalize() == Reciprocal(NthPower(x, n = 2))
    z = NthPower(Exponential(x), n = 2)
    assert z._normalize() == Exponential(Constant(2) * x)
    z = NthPower(Exponential(x, base = 2), n = 3)
    assert z._normalize() == Exponential(Constant(3) * x, base = 2)
