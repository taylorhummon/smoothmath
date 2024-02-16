from pytest import approx, raises
from smoothmath import DomainError, Point
from smoothmath.expression import (
    Variable, Constant, Negation, Multiply, Reciprocal, Power, NthPower, Exponential
)
from assert_partials import ( # type: ignore
    assert_1_ary_partials,
    assert_1_ary_partials_raise,
    assert_2_ary_partials,
    assert_2_ary_partials_raise
)


def test_Power():
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    # at (x, y) = (3, 2.5)
    point = Point(x = 3, y = 2.5)
    assert z.at(point) == approx(15.588457268)
    assert_2_ary_partials(z, point, x, 12.990381056, y, 17.125670716)
    # at (x, y) = (3, 0)
    point = Point(x = 3, y = 0)
    assert z.at(point) == approx(1)
    assert_2_ary_partials(z, point, x, 0, y, 1.0986122886)
    # at (x, y) = (3, -2.5)
    point = Point(x = 3, y = -2.5)
    assert z.at(point) == approx(0.0641500299)
    assert_2_ary_partials(z, point, x, -0.0534583582, y, 0.0704760111)
    # at (x, y) = (0, 2.5)
    point = Point(x = 0, y = 2.5)
    with raises(DomainError):
        z.at(point)
    assert_2_ary_partials_raise(z, point, x, y)
    # at (x, y) = (0, 0)
    point = Point(x = 0, y = 0)
    with raises(DomainError):
        z.at(point)
    assert_2_ary_partials_raise(z, point, x, y)
    # at (x, y) = (0, -2.5)
    point = Point(x = 0, y = -2.5)
    with raises(DomainError):
        z.at(point)
    assert_2_ary_partials_raise(z, point, x, y)
    # at (x, y) = (-3, 2.5)
    point = Point(x = -3, y = 2.5)
    with raises(DomainError):
        z.at(point)
    assert_2_ary_partials_raise(z, point, x, y)
    # at (x, y) = (-3, 0)
    point = Point(x = -3, y = 0)
    with raises(DomainError):
        z.at(point)
    assert_2_ary_partials_raise(z, point, x, y)
    # at (x, y) = (-3, -2.5)
    point = Point(x = -3, y = -2.5)
    with raises(DomainError):
        z.at(point)
    assert_2_ary_partials_raise(z, point, x, y)


def test_Power_composition():
    x = Variable("x")
    y = Variable("y")
    z = Power(Constant(2) * x, Constant(3) * y)
    point = Point(x = 1, y = 1)
    assert z.at(point) == approx(8)
    assert_2_ary_partials(z, point, x, 24, y, 16.63553233343)


def test_Power_with_constant_base_one():
    y = Variable("y")
    z = Power(Constant(1), y)
    # at y = 3
    point = Point(y = 3)
    assert z.at(point) == approx(1)
    assert_1_ary_partials(z, point, y, 0)
    # at y = 0
    point = Point(y = 0)
    assert z.at(point) == approx(1)
    assert_1_ary_partials(z, point, y, 0)
    # at y = -5
    point = Point(y = -5)
    assert z.at(point) == approx(1)
    assert_1_ary_partials(z, point, y, 0)


def test_Power_with_constant_base_zero():
    y = Variable("y")
    z = Power(Constant(0), y)
    # at y = 3
    point = Point(y = 3)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_partials_raise(z, point, y)
    # at y = 0
    point = Point(y = 0)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_partials_raise(z, point, y)
    # at y = -5
    point = Point(y = -5)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_partials_raise(z, point, y)


def test_Power_with_constant_base_negative_one():
    y = Variable("y")
    z = Power(Constant(-1), y)
    # at y = 3
    point = Point(y = 3)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_partials_raise(z, point, y)
    # at y = 0
    point = Point(y = 0)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_partials_raise(z, point, y)
    # at y = -5
    point = Point(y = -5)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_partials_raise(z, point, y)


def test_Power_one_to_the_zero():
    z = Power(Constant(1), Constant(0))
    assert z.at(Point()) == approx(1)


def test_Power_normalization():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    assert z._normalize() == Power(x, y)
    z = Power(x, Constant(1))
    assert z._normalize() == x
    z = Power(x, Constant(0))
    assert z._normalize() == Constant(1)
    z = Power(Constant(1), x)
    assert z._normalize() == Constant(1)
    z = Power(x, Constant(2))
    assert z._normalize() == NthPower(x, n = 2)
    z = Power(x, Constant(3))
    assert z._normalize() == NthPower(x, n = 3)
    z = Power(x, Constant(-1))
    assert z._normalize() == Reciprocal(x)
    z = Power(Constant(2), x)
    assert z._normalize() == Exponential(x, base = 2)
    z = Power(Power(w, x), y)
    assert z._normalize() == Power(w, Multiply(x, y))
    z = Power(Reciprocal(x), y)
    assert z._normalize() == Reciprocal(Power(x, y))
    z = Power(x, Negation(y))
    assert z._normalize() == Reciprocal(Power(x, y))
