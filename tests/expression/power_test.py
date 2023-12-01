from pytest import approx, raises
from smoothmath import DomainError, Point
from smoothmath.expression import Constant, Variable, SquareRoot, Power


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


def test_Power_with_constant_exponent_two():
    x = Variable("x")
    z = Power(x, Constant(2))
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at y = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(9)
    assert z.local_partial(point, x) == approx(6)
    assert global_x_partial.at(point) == approx(6)
    assert z.local_differential(point).component(x) == approx(6)
    assert global_differential.component_at(point, x) == approx(6)
    # at y = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(0)
    assert global_x_partial.at(point) == approx(0)
    assert z.local_differential(point).component(x) == approx(0)
    assert global_differential.component_at(point, x) == approx(0)
    # at y = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(25)
    assert z.local_partial(point, x) == approx(-10)
    assert global_x_partial.at(point) == approx(-10)
    assert z.local_differential(point).component(x) == approx(-10)
    assert global_differential.component_at(point, x) == approx(-10)


def test_Power_with_constant_exponent_two_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(2))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(4)
    assert z.local_partial(point, x) == approx(12)
    assert z.global_partial(x).at(point) == approx(12)
    assert z.local_differential(point).component(x) == approx(12)
    assert z.global_differential().component_at(point, x) == approx(12)


def test_Power_with_constant_exponent_one():
    x = Variable("x")
    z = Power(x, Constant(1))
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at y = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(3)
    assert z.local_partial(point, x) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)
    # at y = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)
    # at y = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(-5)
    assert z.local_partial(point, x) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)


def test_Power_with_constant_exponent_one_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(1))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(point, x) == approx(3)
    assert z.global_partial(x).at(point) == approx(3)
    assert z.local_differential(point).component(x) == approx(3)
    assert z.global_differential().component_at(point, x) == approx(3)


def test_Power_with_constant_exponent_zero():
    x = Variable("x")
    z = Power(x, Constant(0))
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, x) == approx(0)
    assert global_x_partial.at(point) == approx(0)
    assert z.local_differential(point).component(x) == approx(0)
    assert global_differential.component_at(point, x) == approx(0)
    # at x = 0
    point = Point({x: 0})
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
    # at x = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, x) == approx(0)
    assert global_x_partial.at(point) == approx(0)
    assert z.local_differential(point).component(x) == approx(0)
    assert global_differential.component_at(point, x) == approx(0)


def test_Power_with_constant_exponent_zero_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(0))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, x) == approx(0)
    assert z.global_partial(x).at(point) == approx(0)
    assert z.local_differential(point).component(x) == approx(0)
    assert z.global_differential().component_at(point, x) == approx(0)


def test_Power_with_constant_exponent_zero_doesnt_short_circuit():
    x = Variable("x")
    z = Power(SquareRoot(x), Constant(0))
    point = Point({x: -1})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    global_x_partial = z.global_partial(x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    global_differential = z.global_differential()
    with raises(DomainError):
        global_differential.component_at(point, x)


def test_Power_with_constant_exponent_negative_one():
    x = Variable("x")
    z = Power(x, Constant(-1))
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 2
    point = Point({x: 2})
    assert z.evaluate(point) == approx(0.5)
    assert z.local_partial(point, x) == approx(-0.25)
    assert global_x_partial.at(point) == approx(-0.25)
    assert z.local_differential(point).component(x) == approx(-0.25)
    assert global_differential.component_at(point, x) == approx(-0.25)
    # at x = 0
    point = Point({x: 0})
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
    # at x = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(-0.2)
    assert z.local_partial(point, x) == approx(-0.04)
    assert global_x_partial.at(point) == approx(-0.04)
    assert z.local_differential(point).component(x) == approx(-0.04)
    assert global_differential.component_at(point, x) == approx(-0.04)


def test_Power_with_constant_exponent_negative_one_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-1))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(0.5)
    assert z.local_partial(point, x) == approx(-0.75)
    assert z.global_partial(x).at(point) == approx(-0.75)
    assert z.local_differential(point).component(x) == approx(-0.75)
    assert z.global_differential().component_at(point, x) == approx(-0.75)


def test_Power_with_constant_exponent_negative_two():
    x = Variable("x")
    z = Power(x, Constant(-2))
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 2
    point = Point({x: 2})
    assert z.evaluate(point) == approx(0.25)
    assert z.local_partial(point, x) == approx(-0.25)
    assert global_x_partial.at(point) == approx(-0.25)
    assert z.local_differential(point).component(x) == approx(-0.25)
    assert global_differential.component_at(point, x) == approx(-0.25)
    # at x = 0
    point = Point({x: 0})
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
    # at x = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(0.04)
    assert z.local_partial(point, x) == approx(0.016)
    assert global_x_partial.at(point) == approx(0.016)
    assert z.local_differential(point).component(x) == approx(0.016)
    assert global_differential.component_at(point, x) == approx(0.016)


def test_Power_with_constant_exponent_negative_two_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-2))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(0.25)
    assert z.local_partial(point, x) == approx(-0.75)
    assert z.global_partial(x).at(point) == approx(-0.75)
    assert z.local_differential(point).component(x) == approx(-0.75)
    assert z.global_differential().component_at(point, x) == approx(-0.75)


def test_Power_one_to_the_zero():
    z = Power(Constant(1), Constant(0))
    assert z.evaluate(Point({})) == approx(1)


def test_Power_with_exponent_made_from_adding_constants():
    x = Variable("x")
    z = Power(x, Constant(1) + Constant(1))
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(9)
    assert z.local_partial(point, x) == approx(6)
    assert global_x_partial.at(point) == approx(6)
    assert z.local_differential(point).component(x) == approx(6)
    assert global_differential.component_at(point, x) == approx(6)
    # at x = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(0)
    assert global_x_partial.at(point) == approx(0)
    assert z.local_differential(point).component(x) == approx(0)
    assert global_differential.component_at(point, x) == approx(0)
    # at x = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(25)
    assert z.local_partial(point, x) == approx(-10)
    assert global_x_partial.at(point) == approx(-10)
    assert z.local_differential(point).component(x) == approx(-10)
    assert global_differential.component_at(point, x) == approx(-10)


def test_Power_where_exponent_is_an_integer_represented_as_a_float():
    x = Variable("x")
    z = Power(x, Constant(2.0))
    point = Point({x: -5})
    assert z.evaluate(point) == approx(25)
    assert z.local_partial(point, x) == approx(-10)
    assert z.global_partial(x).at(point) == approx(-10)
    assert z.local_differential(point).component(x) == approx(-10)
    assert z.global_differential().component_at(point, x) == approx(-10)
