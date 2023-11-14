from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Logarithm, Divide

def test_Divide():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    variable_values = VariableValues({ x: 5, y: 2 })
    value = z.evaluate(variable_values)
    assert value == approx(2.5)
    partial_with_respect_to_x = z.partial_at(variable_values, x)
    assert partial_with_respect_to_x == approx(0.5)
    partial_with_respect_to_y = z.partial_at(variable_values, y)
    assert partial_with_respect_to_y == approx(-1.25)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0.5)
    assert all_partials.partial_with_respect_to(y) == approx(-1.25)
    variable_values = VariableValues({ x: 3, y: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ x: 0, y: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def test_Divide_composition():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    variable_values = VariableValues({ x: 3, y: 1 })
    value = z.evaluate(variable_values)
    assert value == approx(2)
    partial_with_respect_to_x = z.partial_at(variable_values, x)
    assert partial_with_respect_to_x == approx(0.4)
    partial_with_respect_to_y = z.partial_at(variable_values, y)
    assert partial_with_respect_to_y == approx(-2)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0.4)
    assert all_partials.partial_with_respect_to(y) == approx(-2)

def test_Divide_with_constant_numerator_zero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    variable_values = VariableValues({ y: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)
    variable_values = VariableValues({ y: 0 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)

def test_Divide_with_constant_numerator_zero_composition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    variable_values = VariableValues({ y: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)

def test_Divide_with_constant_numerator_zero_doesnt_short_circuit():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    variable_values = VariableValues({ y: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def test_Divide_with_constant_denominator_one():
    x = Variable("x")
    z = Divide(x, Constant(1))
    variable_values = VariableValues({ x: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(3)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)
    variable_values = VariableValues({ x: 0 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)

def test_divide_with_constant_denominator_zero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    variable_values = VariableValues({ x: 3 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ x: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
