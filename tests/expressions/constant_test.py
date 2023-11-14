from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable

def test_Constant():
    c = Constant(7)
    variable_values = VariableValues({})
    assert c.evaluate(variable_values) == 7
    x = Variable("x")
    variable_values = VariableValues({x: 2})
    partial = c.partial_at(variable_values, x)
    assert partial == 0
    all_partials = c.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == 0
