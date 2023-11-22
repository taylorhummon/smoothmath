from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Logarithm, Divide


def test_Divide():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    synthetic = z.synthetic()
    # at (x, y) = (5, 2)
    variable_values = VariableValues({x: 5, y: 2})
    assert z.evaluate(variable_values) == approx(2.5)
    assert z.partial_at(variable_values, x) == approx(0.5)
    assert z.partial_at(variable_values, y) == approx(-1.25)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(0.5)
    assert both_partials.partial_with_respect_to(y) == approx(-1.25)
    assert synthetic.partial_at(variable_values, x) == approx(0.5)
    assert synthetic.partial_at(variable_values, y) == approx(-1.25)
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
        synthetic.partial_at(variable_values, x)
    with raises(DomainError):
        synthetic.partial_at(variable_values, y)
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
        synthetic.partial_at(variable_values, x)
    with raises(DomainError):
        synthetic.partial_at(variable_values, y)


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
    synthetic = z.synthetic()
    assert synthetic.partial_at(variable_values, x) == approx(0.4)
    assert synthetic.partial_at(variable_values, y) == approx(-2)


def test_Divide_with_constant_numerator_zero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    synthetic = z.synthetic()
    # at y = 3
    variable_values = VariableValues({y: 3})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, y) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(y) == approx(0)
    assert synthetic.partial_at(variable_values, y) == approx(0)
    # at y = 0
    variable_values = VariableValues({y: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic.partial_at(variable_values, y)


def test_Divide_with_constant_numerator_zero_composition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    variable_values = VariableValues({y: 3})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, y) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(y) == approx(0)
    assert z.synthetic().partial_at(variable_values, y) == approx(0)


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
    synthetic = z.synthetic()
    with raises(DomainError):
        synthetic.partial_at(variable_values, y)


def test_Divide_with_constant_denominator_one():
    x = Variable("x")
    z = Divide(x, Constant(1))
    synthetic = z.synthetic()
    # at x = 3
    variable_values = VariableValues({x: 3})
    assert z.evaluate(variable_values) == approx(3)
    assert z.partial_at(variable_values, x) == approx(1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(1)
    assert synthetic.partial_at(variable_values, x) == approx(1)
    # at x = 0
    variable_values = VariableValues({x: 0})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, x) == approx(1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(1)
    assert synthetic.partial_at(variable_values, x) == approx(1)


def test_divide_with_constant_denominator_zero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    synthetic = z.synthetic()
    # at x = 3
    variable_values = VariableValues({x: 3})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic.partial_at(variable_values, x)
    # at x = 0
    variable_values = VariableValues({x: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic.partial_at(variable_values, x)
