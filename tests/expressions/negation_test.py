from pytest import approx
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Negation


def test_Negation():
    x = Variable("x")
    z = Negation(x)
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(-2)
    assert z.partial_at(variable_values, x) == approx(-1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-1)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(-1)


def test_Negation_composition():
    x = Variable("x")
    z = Negation(Constant(2) * x + Constant(1))
    variable_values = VariableValues({x: 3})
    assert z.evaluate(variable_values) == approx(-7)
    assert z.partial_at(variable_values, x) == approx(-2)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-2)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(-2)
