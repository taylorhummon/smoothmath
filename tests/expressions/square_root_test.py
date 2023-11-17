from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, SquareRoot


def test_SquareRoot():
    x = Variable("x")
    z = SquareRoot(x)
    # at x = 4
    variable_values = VariableValues({x: 4})
    value = z.evaluate(variable_values)
    assert value == approx(2)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0.25)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0.25)
    # at x = 0
    variable_values = VariableValues({x: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # at x = -1
    variable_values = VariableValues({x: -1})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)


def test_SquareRoot_composition():
    x = Variable("x")
    z = SquareRoot(Constant(2) * x + Constant(7))
    variable_values = VariableValues({x: 1})
    value = z.evaluate(variable_values)
    assert value == approx(3)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1 / 3)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1 / 3)
