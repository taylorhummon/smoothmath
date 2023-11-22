from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Variable


def test_variable():
    x = Variable("x")
    y = Variable("y")
    variable_values = VariableValues({y: 3})
    assert y.evaluate(variable_values) == 3
    assert y.partial_at(variable_values, x) == 0
    assert y.partial_at(variable_values, y) == 1
    variable_values = VariableValues({x: 2, y: 3})
    all_partials = y.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == 0
    assert all_partials.partial_with_respect_to(y) == 1
    assert y.synthetic_partial(x).evaluate(variable_values) == 0
    assert y.synthetic_partial(y).evaluate(variable_values) == 1
