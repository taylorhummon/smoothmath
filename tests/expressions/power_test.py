from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, SquareRoot, Power


def test_Power():
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    synthetic_partial_with_respect_to_x = z.synthetic_partial(x)
    synthetic_partial_with_respect_to_y = z.synthetic_partial(y)
    # at (x, y) = (3, 2.5)
    variable_values = VariableValues({x: 3, y: 2.5})
    assert z.evaluate(variable_values) == approx(15.588457268)
    assert z.partial_at(variable_values, x) == approx(12.990381056)
    assert z.partial_at(variable_values, y) == approx(17.125670716)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(12.990381056)
    assert both_partials.partial_with_respect_to(y) == approx(17.125670716)
    assert synthetic_partial_with_respect_to_x.evaluate(variable_values) == approx(12.990381056)
    assert synthetic_partial_with_respect_to_y.evaluate(variable_values) == approx(17.125670716)
    # at (x, y) = (3, 0)
    variable_values = VariableValues({x: 3, y: 0})
    assert z.evaluate(variable_values) == approx(1)
    assert z.partial_at(variable_values, x) == approx(0)
    assert z.partial_at(variable_values, y) == approx(1.0986122886)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(0)
    assert both_partials.partial_with_respect_to(y) == approx(1.0986122886)
    assert synthetic_partial_with_respect_to_x.evaluate(variable_values) == approx(0)
    assert synthetic_partial_with_respect_to_y.evaluate(variable_values) == approx(1.0986122886)
    # at (x, y) = (3, -2.5)
    variable_values = VariableValues({x: 3, y: -2.5})
    assert z.evaluate(variable_values) == approx(0.0641500299)
    assert z.partial_at(variable_values, x) == approx(-0.0534583582)
    assert z.partial_at(variable_values, y) == approx(0.0704760111)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(-0.0534583582)
    assert both_partials.partial_with_respect_to(y) == approx(0.0704760111)
    assert synthetic_partial_with_respect_to_x.evaluate(variable_values) == approx(-0.0534583582)
    assert synthetic_partial_with_respect_to_y.evaluate(variable_values) == approx(0.0704760111)
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
    with raises(DomainError):
        synthetic_partial_with_respect_to_x.evaluate(variable_values)
    with raises(DomainError):
        synthetic_partial_with_respect_to_y.evaluate(variable_values)
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
    # # !!! known failure
    # with raises(DomainError):
    #     synthetic_partial_with_respect_to_x.evaluate(variable_values)
    with raises(DomainError):
        synthetic_partial_with_respect_to_y.evaluate(variable_values)
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
    with raises(DomainError):
        synthetic_partial_with_respect_to_x.evaluate(variable_values)
    with raises(DomainError):
        synthetic_partial_with_respect_to_y.evaluate(variable_values)
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
    with raises(DomainError):
        synthetic_partial_with_respect_to_x.evaluate(variable_values)
    with raises(DomainError):
        synthetic_partial_with_respect_to_y.evaluate(variable_values)
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
    # # !!! known failure
    # with raises(DomainError):
    #     synthetic_partial_with_respect_to_x.evaluate(variable_values)
    with raises(DomainError):
        synthetic_partial_with_respect_to_y.evaluate(variable_values)
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
    with raises(DomainError):
        synthetic_partial_with_respect_to_x.evaluate(variable_values)
    with raises(DomainError):
        synthetic_partial_with_respect_to_y.evaluate(variable_values)


def test_Power_composition():
    x = Variable("x")
    y = Variable("y")
    z = Power(Constant(2) * x, Constant(3) * y)
    variable_values = VariableValues({x: 1, y: 1})
    assert z.evaluate(variable_values) == approx(8)
    assert z.partial_at(variable_values, x) == approx(24)
    assert z.partial_at(variable_values, y) == approx(16.63553233343)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(24)
    assert both_partials.partial_with_respect_to(y) == approx(16.63553233343)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(24)
    assert z.synthetic_partial(y).evaluate(variable_values) == approx(16.63553233343)


def test_Power_with_constant_base_one():
    y = Variable("y")
    z = Power(Constant(1), y)
    synthetic_partial = z.synthetic_partial(y)
    # at y = 3
    variable_values = VariableValues({y: 3})
    assert z.evaluate(variable_values) == approx(1)
    assert z.partial_at(variable_values, y) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(y) == approx(0)
    assert synthetic_partial.evaluate(variable_values) == approx(0)
    # at y = 0
    variable_values = VariableValues({y: 0})
    assert z.evaluate(variable_values) == approx(1)
    assert z.partial_at(variable_values, y) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(y) == approx(0)
    assert synthetic_partial.evaluate(variable_values) == approx(0)
    # at y = -5
    variable_values = VariableValues({y: -5})
    assert z.evaluate(variable_values) == approx(1)
    assert z.partial_at(variable_values, y) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(y) == approx(0)
    assert synthetic_partial.evaluate(variable_values) == approx(0)


def test_Power_with_constant_base_zero():
    y = Variable("y")
    z = Power(Constant(0), y)
    synthetic_partial = z.synthetic_partial(y)
    # at y = 3
    variable_values = VariableValues({y: 3})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)
    # at y = 0
    variable_values = VariableValues({y: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)
    # at y = -5
    variable_values = VariableValues({y: -5})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)


def test_Power_with_constant_base_negative_one():
    y = Variable("y")
    z = Power(Constant(-1), y)
    synthetic_partial = z.synthetic_partial(y)
    # at y = 3
    variable_values = VariableValues({y: 3})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)
    # at y = 0
    variable_values = VariableValues({y: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)
    # at y = -5
    variable_values = VariableValues({y: -5})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)


def test_Power_with_constant_exponent_two():
    x = Variable("x")
    z = Power(x, Constant(2))
    synthetic_partial = z.synthetic_partial(x)
    # at y = 3
    variable_values = VariableValues({x: 3})
    assert z.evaluate(variable_values) == approx(9)
    assert z.partial_at(variable_values, x) == approx(6)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(6)
    assert synthetic_partial.evaluate(variable_values) == approx(6)
    # at y = 0
    variable_values = VariableValues({x: 0})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, x) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(0)
    assert synthetic_partial.evaluate(variable_values) == approx(0)
    # at y = -5
    variable_values = VariableValues({x: -5})
    assert z.evaluate(variable_values) == approx(25)
    assert z.partial_at(variable_values, x) == approx(-10)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-10)
    assert synthetic_partial.evaluate(variable_values) == approx(-10)


def test_Power_with_constant_exponent_two_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(2))
    variable_values = VariableValues({x: 1})
    assert z.evaluate(variable_values) == approx(4)
    assert z.partial_at(variable_values, x) == approx(12)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(12)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(12)


def test_Power_with_constant_exponent_one():
    x = Variable("x")
    z = Power(x, Constant(1))
    synthetic_partial = z.synthetic_partial(x)
    # at y = 3
    variable_values = VariableValues({x: 3})
    assert z.evaluate(variable_values) == approx(3)
    assert z.partial_at(variable_values, x) == approx(1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(1)
    assert synthetic_partial.evaluate(variable_values) == approx(1)
    # at y = 0
    variable_values = VariableValues({x: 0})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, x) == approx(1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(1)
    assert synthetic_partial.evaluate(variable_values) == approx(1)
    # at y = -5
    variable_values = VariableValues({x: -5})
    assert z.evaluate(variable_values) == approx(-5)
    assert z.partial_at(variable_values, x) == approx(1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(1)
    assert synthetic_partial.evaluate(variable_values) == approx(1)


def test_Power_with_constant_exponent_one_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(1))
    variable_values = VariableValues({x: 1})
    assert z.evaluate(variable_values) == approx(2)
    assert z.partial_at(variable_values, x) == approx(3)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(3)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(3)


def test_Power_with_constant_exponent_zero():
    x = Variable("x")
    z = Power(x, Constant(0))
    synthetic_partial = z.synthetic_partial(x)
    # at x = 3
    variable_values = VariableValues({x: 3})
    assert z.evaluate(variable_values) == approx(1)
    assert z.partial_at(variable_values, x) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(0)
    assert synthetic_partial.evaluate(variable_values) == approx(0)
    # at x = 0
    variable_values = VariableValues({x: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # # !!! known failure
    # with raises(DomainError):
    #     synthetic_partial.evaluate(variable_values)
    # at x = -5
    variable_values = VariableValues({x: -5})
    assert z.evaluate(variable_values) == approx(1)
    assert z.partial_at(variable_values, x) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(0)
    assert synthetic_partial.evaluate(variable_values) == approx(0)


def test_Power_with_constant_exponent_zero_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(0))
    variable_values = VariableValues({x: 1})
    assert z.evaluate(variable_values) == approx(1)
    assert z.partial_at(variable_values, x) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(0)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(0)


def test_Power_with_constant_exponent_zero_doesnt_short_circuit():
    x = Variable("x")
    z = Power(SquareRoot(x), Constant(0))
    variable_values = VariableValues({x: -1})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # # !!! known failure
    # synthetic_partial = z.synthetic_partial(x)
    # with raises(DomainError):
    #     synthetic_partial.evaluate(variable_values)


def test_Power_with_constant_exponent_negative_one():
    x = Variable("x")
    z = Power(x, Constant(-1))
    synthetic_partial = z.synthetic_partial(x)
    # at x = 2
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(0.5)
    assert z.partial_at(variable_values, x) == approx(-0.25)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-0.25)
    assert synthetic_partial.evaluate(variable_values) == approx(-0.25)
    # at x = 0
    variable_values = VariableValues({x: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)
    # at x = -5
    variable_values = VariableValues({x: -5})
    assert z.evaluate(variable_values) == approx(-0.2)
    assert z.partial_at(variable_values, x) == approx(-0.04)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-0.04)
    assert synthetic_partial.evaluate(variable_values) == approx(-0.04)


def test_Power_with_constant_exponent_negative_one_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-1))
    variable_values = VariableValues({x: 1})
    assert z.evaluate(variable_values) == approx(0.5)
    assert z.partial_at(variable_values, x) == approx(-0.75)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-0.75)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(-0.75)


def test_Power_with_constant_exponent_negative_two():
    x = Variable("x")
    z = Power(x, Constant(-2))
    synthetic_partial = z.synthetic_partial(x)
    # at x = 2
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(0.25)
    assert z.partial_at(variable_values, x) == approx(-0.25)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-0.25)
    assert synthetic_partial.evaluate(variable_values) == approx(-0.25)
    # at x = 0
    variable_values = VariableValues({x: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)
    # at x = -5
    variable_values = VariableValues({x: -5})
    assert z.evaluate(variable_values) == approx(0.04)
    assert z.partial_at(variable_values, x) == approx(0.016)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(0.016)
    assert synthetic_partial.evaluate(variable_values) == approx(0.016)


def test_Power_with_constant_exponent_negative_two_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-2))
    variable_values = VariableValues({x: 1})
    assert z.evaluate(variable_values) == approx(0.25)
    assert z.partial_at(variable_values, x) == approx(-0.75)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-0.75)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(-0.75)


def test_Power_one_to_the_zero():
    z = Power(Constant(1), Constant(0))
    assert z.evaluate(VariableValues({})) == approx(1)


def test_Power_with_exponent_made_from_adding_constants():
    x = Variable("x")
    z = Power(x, Constant(1) + Constant(1))
    synthetic_partial = z.synthetic_partial(x)
    # at x = 3
    variable_values = VariableValues({x: 3})
    assert z.evaluate(variable_values) == approx(9)
    assert z.partial_at(variable_values, x) == approx(6)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(6)
    assert synthetic_partial.evaluate(variable_values) == approx(6)
    # at x = 0
    variable_values = VariableValues({x: 0})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, x) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(0)
    assert synthetic_partial.evaluate(variable_values) == approx(0)
    # at x = -5
    variable_values = VariableValues({x: -5})
    assert z.evaluate(variable_values) == approx(25)
    assert z.partial_at(variable_values, x) == approx(-10)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-10)
    assert synthetic_partial.evaluate(variable_values) == approx(-10)


def test_Power_where_exponent_is_an_integer_represented_as_a_float():
    x = Variable("x")
    z = Power(x, Constant(2.0))
    variable_values = VariableValues({x: -5})
    assert z.evaluate(variable_values) == approx(25)
    assert z.partial_at(variable_values, x) == approx(-10)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-10)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(-10)
