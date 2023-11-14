from pytest import approx
from smoothmath.variable_values import VariableValues
from smoothmath.expressions.constant import Constant
from smoothmath.expressions.variable import Variable
from smoothmath.expressions.minus import Minus

def test_Minus():
    x = Variable("x")
    y = Variable("y")
    z = Minus(x, y)
    variable_values = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(-1)
    partial_with_respect_toX = z.partial_at(variable_values, x)
    assert partial_with_respect_toX == approx(1)
    partial_with_respect_toY = z.partial_at(variable_values, y)
    assert partial_with_respect_toY == approx(-1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)
    assert all_partials.partial_with_respect_to(y) == approx(-1)

def test_Minus_composition():
    x = Variable("x")
    y = Variable("y")
    z = Minus(Constant(5) * x, Constant(4) * y)
    variable_values = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(-2)
    partial_with_respect_toX = z.partial_at(variable_values, x)
    assert partial_with_respect_toX == approx(5)
    partial_with_respect_toY = z.partial_at(variable_values, y)
    assert partial_with_respect_toY == approx(-4)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(5)
    assert all_partials.partial_with_respect_to(y) == approx(-4)
