from pytest import approx
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Plus

def test_Plus():
    x = Variable("x")
    y = Variable("y")
    z = Plus(x, y)
    variable_values = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(5)
    partial_with_respect_to_x = z.partial_at(variable_values, x)
    assert partial_with_respect_to_x == approx(1)
    partial_with_respect_to_y = z.partial_at(variable_values, y)
    assert partial_with_respect_to_y == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)
    assert all_partials.partial_with_respect_to(y) == approx(1)

def test_Plus_composition():
    x = Variable("x")
    y = Variable("y")
    z = Plus(Constant(5) * x, Constant(4) * y)
    variable_values = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(22)
    partial_with_respect_to_x = z.partial_at(variable_values, x)
    assert partial_with_respect_to_x == approx(5)
    partial_with_respect_to_y = z.partial_at(variable_values, y)
    assert partial_with_respect_to_y == approx(4)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(5)
    assert all_partials.partial_with_respect_to(y) == approx(4)
