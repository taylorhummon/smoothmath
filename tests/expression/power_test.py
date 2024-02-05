from pytest import approx, raises
from smoothmath import DomainError, Point
from smoothmath.expression import (
  Constant, Variable, Negation, Reciprocal, NthPower, Exponential, Multiply, Power
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
