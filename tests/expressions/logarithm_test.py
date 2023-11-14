from pytest import approx, raises
import math
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Logarithm

def test_Logarithm():
    x = Variable("x")
    z = Logarithm(x)
    variable_values = VariableValues({ x: 1 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)
    variable_values = VariableValues({ x: math.e })
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1 / math.e)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1 / math.e)
    variable_values = VariableValues({ x: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ x: -1 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def test_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(3))
    variable_values = VariableValues({ x: 2 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(2)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(2)

def test_base_two_Logarithm():
    x = Variable("x")
    z = Logarithm(x, 2)
    variable_values = VariableValues({ x: 1 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1.442695040888)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1.442695040888)
    variable_values = VariableValues({ x: 2 })
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0.721347520444)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0.721347520444)
    variable_values = VariableValues({ x: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ x: -1 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def test_base_two_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(6), 2)
    variable_values = VariableValues({ x: 7 })
    value = z.evaluate(variable_values)
    assert value == approx(3)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0.3606737602222)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0.3606737602222)
