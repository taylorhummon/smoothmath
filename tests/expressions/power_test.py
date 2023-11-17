from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, SquareRoot, Logarithm, Power


def test_Power():
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    # at (x, y) = (3, 2.5)
    variable_values = VariableValues({x: 3, y: 2.5})
    value = z.evaluate(variable_values)
    assert value == approx(15.588457268)
    partial_with_respect_to_x = z.partial_at(variable_values, x)
    assert partial_with_respect_to_x == approx(12.990381056)
    partial_with_respect_to_y = z.partial_at(variable_values, y)
    assert partial_with_respect_to_y == approx(17.125670716)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(12.990381056)
    assert all_partials.partial_with_respect_to(y) == approx(17.125670716)
    # at (x, y) = (3, 0)
    variable_values = VariableValues({x: 3, y: 0})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial_with_respect_to_x = z.partial_at(variable_values, x)
    assert partial_with_respect_to_x == approx(0)
    partial_with_respect_to_y = z.partial_at(variable_values, y)
    assert partial_with_respect_to_y == approx(1.0986122886)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)
    assert all_partials.partial_with_respect_to(y) == approx(1.0986122886)
    # at (x, y) = (3, -2.5)
    variable_values = VariableValues({x: 3, y: -2.5})
    value = z.evaluate(variable_values)
    assert value == approx(0.0641500299)
    partial_with_respect_to_x = z.partial_at(variable_values, x)
    assert partial_with_respect_to_x == approx(-0.0534583582)
    partial_with_respect_to_y = z.partial_at(variable_values, y)
    assert partial_with_respect_to_y == approx(0.0704760111)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.0534583582)
    assert all_partials.partial_with_respect_to(y) == approx(0.0704760111)
    # at (x, y) = (0, 2.5)
    variable_values = VariableValues({x: 0, y: 2.5})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at (x, y) = (0, 0)
    variable_values = VariableValues({x: 0, y: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at (x, y) = (0, -2.5)
    variable_values = VariableValues({x: 0, y: -2.5})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at (x, y) = (-3, 2.5)
    variable_values = VariableValues({x: -3, y: 2.5})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at (x, y) = (-3, 0)
    variable_values = VariableValues({x: -3, y: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at (x, y) = (-3, -2.5)
    variable_values = VariableValues({x: -3, y: -2.5})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)


def test_Power_composition():
    x = Variable("x")
    y = Variable("y")
    z = Power(Constant(2) * x, Constant(3) * y)
    variable_values = VariableValues({x: 1, y: 1})
    value = z.evaluate(variable_values)
    assert value == approx(8)
    partial_with_respect_to_x = z.partial_at(variable_values, x)
    assert partial_with_respect_to_x == approx(24)
    partial_with_respect_to_y = z.partial_at(variable_values, y)
    assert partial_with_respect_to_y == approx(16.63553233343)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(24)
    assert all_partials.partial_with_respect_to(y) == approx(16.63553233343)


def test_Power_with_constant_base_one():
    y = Variable("y")
    z = Power(Constant(1), y)
    # at y = 3
    variable_values = VariableValues({y: 3})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)
    # at y = 0
    variable_values = VariableValues({y: 0})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)
    # at y = -5
    variable_values = VariableValues({y: -5})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)


def test_Power_with_constant_base_one_doesnt_short_circuit():
    x = Variable("x")
    z = Power(Constant(1), SquareRoot(x))
    variable_values = VariableValues({x: -1})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)


def test_Power_with_constant_base_zero():
    y = Variable("y")
    z = Power(Constant(0), y)
    # at y = 3
    variable_values = VariableValues({y: 3})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at y = 0
    variable_values = VariableValues({y: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at y = -5
    variable_values = VariableValues({y: -5})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)


def test_Power_with_constant_base_negative_one():
    y = Variable("y")
    z = Power(Constant(-1), y)
    # at y = 3
    variable_values = VariableValues({y: 3})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at y = 0
    variable_values = VariableValues({y: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at y = -5
    variable_values = VariableValues({y: -5})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)


def test_Power_with_constant_exponent_two():
    x = Variable("x")
    z = Power(x, Constant(2))
    # at y = 3
    variable_values = VariableValues({x: 3})
    value = z.evaluate(variable_values)
    assert value == approx(9)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(6)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(6)
    # at y = 0
    variable_values = VariableValues({x: 0})
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)
    # at y = -5
    variable_values = VariableValues({x: -5})
    value = z.evaluate(variable_values)
    assert value == approx(25)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-10)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-10)


def test_Power_with_constant_exponent_two_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(2))
    variable_values = VariableValues({x: 1})
    value = z.evaluate(variable_values)
    assert value == approx(4)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(12)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(12)


def test_Power_with_constant_exponent_one():
    x = Variable("x")
    z = Power(x, Constant(1))
    # at y = 3
    variable_values = VariableValues({x: 3})
    value = z.evaluate(variable_values)
    assert value == approx(3)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)
    # at y = 0
    variable_values = VariableValues({x: 0})
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)
    # at y = -5
    variable_values = VariableValues({x: -5})
    value = z.evaluate(variable_values)
    assert value == approx(-5)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)


def test_Power_with_constant_exponent_one_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(1))
    variable_values = VariableValues({x: 1})
    value = z.evaluate(variable_values)
    assert value == approx(2)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(3)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(3)


def test_Power_with_constant_exponent_zero():
    x = Variable("x")
    z = Power(x, Constant(0))
    # at x = 3
    variable_values = VariableValues({x: 3})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)
    # at x = 0
    variable_values = VariableValues({x: 0})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)
    # at x = -5
    variable_values = VariableValues({x: -5})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)


def test_Power_with_constant_exponent_zero_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(0))
    variable_values = VariableValues({x: 1})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)


def test_Power_with_constant_exponent_zero_doesnt_short_circuit():
    x = Variable("x")
    z = Power(Logarithm(x), Constant(0))
    variable_values = VariableValues({x: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)


def test_Power_with_constant_exponent_negative_one():
    x = Variable("x")
    z = Power(x, Constant(-1))
    # at x = 2
    variable_values = VariableValues({x: 2})
    value = z.evaluate(variable_values)
    assert value == approx(0.5)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-0.25)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.25)
    # at x = 0
    variable_values = VariableValues({x: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at x = -5
    variable_values = VariableValues({x: -5})
    value = z.evaluate(variable_values)
    assert value == approx(-0.2)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-0.04)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.04)


def test_Power_with_constant_exponent_negative_one_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-1))
    variable_values = VariableValues({x: 1})
    value = z.evaluate(variable_values)
    assert value == approx(0.5)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-0.75)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.75)


def test_Power_with_constant_exponent_negative_two():
    x = Variable("x")
    z = Power(x, Constant(-2))
    # at x = 2
    variable_values = VariableValues({x: 2})
    value = z.evaluate(variable_values)
    assert value == approx(0.25)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-0.25)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.25)
    # at x = 0
    variable_values = VariableValues({x: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at x = -5
    variable_values = VariableValues({x: -5})
    value = z.evaluate(variable_values)
    assert value == approx(0.04)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0.016)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0.016)


def test_Power_with_constant_exponent_negative_two_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-2))
    variable_values = VariableValues({x: 1})
    value = z.evaluate(variable_values)
    assert value == approx(0.25)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-0.75)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.75)


def test_Power_with_exponent_made_from_adding_constants():
    x = Variable("x")
    z = Power(x, Constant(1) + Constant(1))
    # at x = 3
    variable_values = VariableValues({x: 3})
    value = z.evaluate(variable_values)
    assert value == approx(9)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(6)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(6)
    # at x = 0
    variable_values = VariableValues({x: 0})
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)
    # at x = -5
    variable_values = VariableValues({x: -5})
    value = z.evaluate(variable_values)
    assert value == approx(25)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-10)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-10)


def test_Power_where_exponent_is_an_integer_represented_as_a_float():
    x = Variable("x")
    z = Power(x, Constant(2.0))
    variable_values = VariableValues({x: -5})
    value = z.evaluate(variable_values)
    assert value == approx(25)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-10)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-10)
