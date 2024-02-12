from pytest import approx, raises
import math
from smoothmath import DomainError, Point
from smoothmath.expression import (
    Variable, Constant, Negation, Multiply, Reciprocal, NthPower, Exponential, Logarithm
)


def test_Logarithm():
    x = Variable("x")
    z = Logarithm(x)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 1
    point = Point(x = 1)
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)
    # at x = e
    point = Point(x = math.e)
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, x) == approx(1 / math.e)
    assert global_x_partial.at(point) == approx(1 / math.e)
    assert z.local_differential(point).component(x) == approx(1 / math.e)
    assert global_differential.component_at(point, x) == approx(1 / math.e)
    # at x = 0
    point = Point(x = 0)
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    # at x = -1
    point = Point(x = -1)
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)


def test_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(3))
    point = Point(x = 2)
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(2)
    assert z.global_partial(x).at(point) == approx(2)
    assert z.local_differential(point).component(x) == approx(2)
    assert z.global_differential().component_at(point, x) == approx(2)


def test_base_two_Logarithm():
    x = Variable("x")
    z = Logarithm(x, base = 2)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 1
    point = Point(x = 1)
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(1.442695040888)
    assert global_x_partial.at(point) == approx(1.442695040888)
    assert z.local_differential(point).component(x) == approx(1.442695040888)
    assert global_differential.component_at(point, x) == approx(1.442695040888)
    # at x = 2
    point = Point(x = 2)
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, x) == approx(0.721347520444)
    assert global_x_partial.at(point) == approx(0.721347520444)
    assert z.local_differential(point).component(x) == approx(0.721347520444)
    assert global_differential.component_at(point, x) == approx(0.721347520444)
    # at x = 0
    point = Point(x = 0)
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    # at x = -1
    point = Point(x = -1)
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)


def test_base_two_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(6), base = 2)
    point = Point(x = 7)
    assert z.evaluate(point) == approx(3)
    assert z.local_partial(point, x) == approx(0.3606737602222)
    assert z.global_partial(x).at(point) == approx(0.3606737602222)
    assert z.local_differential(point).component(x) == approx(0.3606737602222)
    assert z.global_differential().component_at(point, x) == approx(0.3606737602222)


def test_Logarithm_equality():
    x = Variable("x")
    y = Variable("y")
    assert Logarithm(x) == Logarithm(x)
    assert Logarithm(x) != Logarithm(y)
    assert Logarithm(x) == Logarithm(x, base = math.e)
    assert Logarithm(x, base = 2) == Logarithm(x, base = 2)
    assert Logarithm(x, base = 2) != Logarithm(x, base = 3)
    assert Logarithm(x, base = 2) != Logarithm(x)


def test_Logarithm_normalization():
    x = Variable("x")
    y = Variable("y")
    z = Logarithm(x)
    assert z._normalize() == Logarithm(x)
    z = Logarithm(Exponential(x))
    assert z._normalize() == x
    z = Logarithm(Exponential(x, base = 2), base = 2)
    assert z._normalize() == x
    z = Logarithm(Exponential(x, base = 3), base = 2)
    assert z._normalize() == Logarithm(Exponential(x, base = 3), base = 2)
    z = Logarithm(Reciprocal(x))
    assert z._normalize() == Negation(Logarithm(x))
    z = Logarithm(Reciprocal(x), base = 2)
    assert z._normalize() == Negation(Logarithm(x, base = 2))
    z = Logarithm(NthPower(x, n = 3))
    assert z._normalize() == Constant(3) * Logarithm(x)
    z = Logarithm(NthPower(x, n = 3), base = 2)
    assert z._normalize() == Constant(3) * Logarithm(x, base = 2)
    z = Logarithm(NthPower(x, n = 4))
    # We don't want to reduce to Multiply(Constant(4), Logarithm(u)) because u might be negative
    assert z._normalize() == Logarithm(NthPower(x, n = 4))
    z = Logarithm(Multiply(x, y))
    assert z._normalize() == Logarithm(Multiply(x, y))
