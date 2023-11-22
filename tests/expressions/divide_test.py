from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Logarithm, Divide


def test_Divide():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    synthetic_partial_with_respect_to_x = z.synthetic_partial(x)
    synthetic_partial_with_respect_to_y = z.synthetic_partial(y)
    # at (x, y) = (5, 2)
    variable_values = VariableValues({x: 5, y: 2})
    assert z.evaluate(variable_values) == approx(2.5)
    assert z.partial_at(variable_values, x) == approx(0.5)
    assert z.partial_at(variable_values, y) == approx(-1.25)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(0.5)
    assert both_partials.partial_with_respect_to(y) == approx(-1.25)
    assert synthetic_partial_with_respect_to_x.evaluate(variable_values) == approx(0.5)
    assert synthetic_partial_with_respect_to_y.evaluate(variable_values) == approx(-1.25)
    # at (x, y) = (3, 0)
    variable_values = VariableValues({x: 3, y: 0})
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
    with raises(DomainError):
        synthetic_partial_with_respect_to_x.evaluate(variable_values)
    with raises(DomainError):
        synthetic_partial_with_respect_to_y.evaluate(variable_values)


def test_Divide_composition():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    variable_values = VariableValues({x: 3, y: 1})
    assert z.evaluate(variable_values) == approx(2)
    assert z.partial_at(variable_values, x) == approx(0.4)
    assert z.partial_at(variable_values, y) == approx(-2)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(0.4)
    assert both_partials.partial_with_respect_to(y) == approx(-2)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(0.4)
    assert z.synthetic_partial(y).evaluate(variable_values) == approx(-2)


def test_Divide_with_constant_numerator_zero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    synthetic_partial = z.synthetic_partial(y)
    # at y = 3
    variable_values = VariableValues({y: 3})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, y) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(y) == approx(0)
    assert synthetic_partial.evaluate(variable_values) == approx(0)
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


def test_Divide_with_constant_numerator_zero_composition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    variable_values = VariableValues({y: 3})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, y) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(y) == approx(0)
    assert z.synthetic_partial(y).evaluate(variable_values) == approx(0)


def test_Divide_with_constant_numerator_zero_doesnt_short_circuit():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    variable_values = VariableValues({y: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    synthetic_partial = z.synthetic_partial(y)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)


def test_Divide_with_constant_denominator_one():
    x = Variable("x")
    z = Divide(x, Constant(1))
    synthetic_partial = z.synthetic_partial(x)
    # at x = 3
    variable_values = VariableValues({x: 3})
    assert z.evaluate(variable_values) == approx(3)
    assert z.partial_at(variable_values, x) == approx(1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(1)
    assert synthetic_partial.evaluate(variable_values) == approx(1)
    # at x = 0
    variable_values = VariableValues({x: 0})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, x) == approx(1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(1)
    assert synthetic_partial.evaluate(variable_values) == approx(1)


def test_divide_with_constant_denominator_zero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    synthetic_partial = z.synthetic_partial(x)
    # at x = 3
    variable_values = VariableValues({x: 3})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)
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
