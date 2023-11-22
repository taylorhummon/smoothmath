from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable


def test_Constant():
    c = Constant(7)
    variable_values = VariableValues({})
    assert c.evaluate(variable_values) == 7
    x = Variable("x")
    variable_values = VariableValues({x: 2})
    assert c.partial_at(variable_values, x) == 0
    assert c.all_partials_at(variable_values).partial_with_respect_to(x) == 0
    assert c.synthetic().partial_at(variable_values, x) == 0
