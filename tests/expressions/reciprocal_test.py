from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Reciprocal


def test_Reciprocal():
    x = Variable("x")
    z = Reciprocal(x)
    # at x = 2
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(0.5)
    assert z.partial_at(variable_values, x) == approx(-0.25)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-0.25)
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
    assert z.evaluate(variable_values) == approx(-1)
    assert z.partial_at(variable_values, x) == approx(-1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-1)


def test_Reciprocal_composition():
    x = Variable("x")
    z = Reciprocal(Constant(2) * x - Constant(4))
    variable_values = VariableValues({x: 3})
    assert z.evaluate(variable_values) == approx(0.5)
    assert z.partial_at(variable_values, x) == approx(-0.5)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-0.5)
