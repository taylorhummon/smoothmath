from pytest import approx, raises
from smoothmath import DomainError, Point
from smoothmath.expression import (
  Constant, Variable, Negation, Reciprocal, NthPower, NthRoot, Exponential, Multiply, Power
)


def test_Power():
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    global_x_partial = z.global_partial(x)
    global_y_partial = z.global_partial(y)
    global_differential = z.global_differential()
    # at (x, y) = (3, 2.5)
    point = Point({x: 3, y: 2.5})
    assert z.evaluate(point) == approx(15.588457268)
    assert z.local_partial(point, x) == approx(12.990381056)
    assert z.local_partial(point, y) == approx(17.125670716)
    assert global_x_partial.at(point) == approx(12.990381056)
    assert global_y_partial.at(point) == approx(17.125670716)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(12.990381056)
    assert local_differential.component(y) == approx(17.125670716)
    assert global_differential.component_at(point, x) == approx(12.990381056)
    assert global_differential.component_at(point, y) == approx(17.125670716)
    # at (x, y) = (3, 0)
    point = Point({x: 3, y: 0})
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, x) == approx(0)
    assert z.local_partial(point, y) == approx(1.0986122886)
    assert global_x_partial.at(point) == approx(0)
    assert global_y_partial.at(point) == approx(1.0986122886)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(0)
    assert local_differential.component(y) == approx(1.0986122886)
    assert global_differential.component_at(point, x) == approx(0)
    assert global_differential.component_at(point, y) == approx(1.0986122886)
    # at (x, y) = (3, -2.5)
    point = Point({x: 3, y: -2.5})
    assert z.evaluate(point) == approx(0.0641500299)
    assert z.local_partial(point, x) == approx(-0.0534583582)
    assert z.local_partial(point, y) == approx(0.0704760111)
    assert global_x_partial.at(point) == approx(-0.0534583582)
    assert global_y_partial.at(point) == approx(0.0704760111)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(-0.0534583582)
    assert local_differential.component(y) == approx(0.0704760111)
    assert global_differential.component_at(point, x) == approx(-0.0534583582)
    assert global_differential.component_at(point, y) == approx(0.0704760111)
    # at (x, y) = (0, 2.5)
    point = Point({x: 0, y: 2.5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    with raises(DomainError):
        global_differential.component_at(point, y)
    # at (x, y) = (0, 0)
    point = Point({x: 0, y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    with raises(DomainError):
        global_differential.component_at(point, y)
    # at (x, y) = (0, -2.5)
    point = Point({x: 0, y: -2.5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    with raises(DomainError):
        global_differential.component_at(point, y)
    # at (x, y) = (-3, 2.5)
    point = Point({x: -3, y: 2.5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    with raises(DomainError):
        global_differential.component_at(point, y)
    # at (x, y) = (-3, 0)
    point = Point({x: -3, y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    with raises(DomainError):
        global_differential.component_at(point, y)
    # at (x, y) = (-3, -2.5)
    point = Point({x: -3, y: -2.5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    with raises(DomainError):
        global_differential.component_at(point, y)


def test_Power_composition():
    x = Variable("x")
    y = Variable("y")
    z = Power(Constant(2) * x, Constant(3) * y)
    point = Point({x: 1, y: 1})
    assert z.evaluate(point) == approx(8)
    assert z.local_partial(point, x) == approx(24)
    assert z.local_partial(point, y) == approx(16.63553233343)
    assert z.global_partial(x).at(point) == approx(24)
    assert z.global_partial(y).at(point) == approx(16.63553233343)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(24)
    assert local_differential.component(y) == approx(16.63553233343)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(24)
    assert global_differential.component_at(point, y) == approx(16.63553233343)


def test_Power_with_constant_base_one():
    y = Variable("y")
    z = Power(Constant(1), y)
    global_y_partial = z.global_partial(y)
    global_differential = z.global_differential()
    # at y = 3
    point = Point({y: 3})
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, y) == approx(0)
    assert global_y_partial.at(point) == approx(0)
    assert z.local_differential(point).component(y) == approx(0)
    assert global_differential.component_at(point, y) == approx(0)
    # at y = 0
    point = Point({y: 0})
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, y) == approx(0)
    assert global_y_partial.at(point) == approx(0)
    assert z.local_differential(point).component(y) == approx(0)
    assert global_differential.component_at(point, y) == approx(0)
    # at y = -5
    point = Point({y: -5})
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, y) == approx(0)
    assert global_y_partial.at(point) == approx(0)
    assert z.local_differential(point).component(y) == approx(0)
    assert global_differential.component_at(point, y) == approx(0)


def test_Power_with_constant_base_zero():
    y = Variable("y")
    z = Power(Constant(0), y)
    global_y_partial = z.global_partial(y)
    global_differential = z.global_differential()
    # at y = 3
    point = Point({y: 3})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, y)
    # at y = 0
    point = Point({y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, y)
    # at y = -5
    point = Point({y: -5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, y)


def test_Power_with_constant_base_negative_one():
    y = Variable("y")
    z = Power(Constant(-1), y)
    global_y_partial = z.global_partial(y)
    global_differential = z.global_differential()
    # at y = 3
    point = Point({y: 3})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, y)
    # at y = 0
    point = Point({y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, y)
    # at y = -5
    point = Point({y: -5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, y)


def test_Power_one_to_the_zero():
    z = Power(Constant(1), Constant(0))
    assert z.evaluate(Point({})) == approx(1)


def test_reduce_u_to_the_one():
    u = Variable("u")
    z = Power(u, Constant(1))
    assert z._reduce_u_to_the_one() == u


def test_reduce_u_to_the_zero():
    u = Variable("u")
    z = Power(u, Constant(0))
    assert z._reduce_u_to_the_zero() == Constant(1)


def test_reduce_one_to_the_u():
    u = Variable("u")
    z = Power(Constant(1), u)
    assert z._reduce_one_to_the_u() == Constant(1)


def test_reduce_u_to_the_n_at_least_two():
    u = Variable("u")
    z = Power(u, Constant(2))
    assert z._reduce_u_to_the_n_at_least_two() == NthPower(u, n = 2)
    z = Power(u, Constant(3))
    assert z._reduce_u_to_the_n_at_least_two() == NthPower(u, n = 3)


def test_reduce_u_to_the_negative_one():
    u = Variable("u")
    z = Power(u, Constant(-1))
    assert z._reduce_u_to_the_negative_one() == Reciprocal(u)


def test_reduce_u_to_the_one_over_n():
    u = Variable("u")
    z = Power(u, Reciprocal(Constant(2)))
    assert z._reduce_u_to_the_one_over_n() == NthRoot(u, n = 2)
    z = Power(u, Reciprocal(Constant(3)))
    assert z._reduce_u_to_the_one_over_n() == NthRoot(u, n = 3)


def test_reduce_power_with_constant_base():
    u = Variable("u")
    z = Power(Constant(2), u)
    assert z._reduce_power_with_constant_base() == Exponential(u, base = 2)


def test_reduce_power_of_power():
    u = Variable("u")
    v = Variable("v")
    w = Variable("w")
    z = Power(Power(u, v), w)
    assert z._reduce_power_of_power() == Power(u, Multiply(v, w))


def test_reduce_u_to_the_negation_of_v():
    u = Variable("u")
    v = Variable("v")
    z = Power(u, Negation(v))
    assert z._reduce_u_to_the_negation_of_v() == Reciprocal(Power(u, v))


def test_reduce_one_over_u__to_the_v():
    u = Variable("u")
    v = Variable("v")
    z = Power(Reciprocal(u), v)
    assert z._reduce_one_over_u__to_the_v() == Reciprocal(Power(u, v))
