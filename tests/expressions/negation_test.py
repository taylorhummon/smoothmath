from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Negation

def test_Negation():
    x = Variable("x")
    z = Negation(x)
    variable_values = VariableValues({x: 2})
    value = z.evaluate(variable_values)
    assert value == -2
    partial = z.partial_at(variable_values, x)
    assert partial == -1
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == -1

def test_Negation_composition():
    x = Variable("x")
    z = Negation(Constant(2) * x + Constant(1))
    variable_values = VariableValues({x: 3})
    value = z.evaluate(variable_values)
    assert value == -7
    partial = z.partial_at(variable_values, x)
    assert partial == -2
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == -2
