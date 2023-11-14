from smoothmath.expressions.variable import Variable
from smoothmath.variable_values import VariableValues

def test_variable():
    x = Variable("x")
    variable_values = VariableValues({ x: 2 })
    value = x.evaluate(variable_values)
    assert value == 2
    partial = x.partial_at(variable_values, x)
    assert partial == 1
    y = Variable("y")
    variable_values = VariableValues({ x: 2, y: 3 })
    all_partials = x.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == 1
    assert all_partials.partial_with_respect_to(y) == 0
