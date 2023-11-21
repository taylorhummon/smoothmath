from pytest import approx
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Plus


def test_Plus():
    x = Variable("x")
    y = Variable("y")
    z = Plus(x, y)
    variable_values = VariableValues({x: 2, y: 3})
    assert z.evaluate(variable_values) == approx(5)
    assert z.partial_at(variable_values, x) == approx(1)
    assert z.partial_at(variable_values, y) == approx(1)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(1)
    assert both_partials.partial_with_respect_to(y) == approx(1)


def test_Plus_composition():
    x = Variable("x")
    y = Variable("y")
    z = Plus(Constant(5) * x, Constant(4) * y)
    variable_values = VariableValues({x: 2, y: 3})
    assert z.evaluate(variable_values) == approx(22)
    assert z.partial_at(variable_values, x) == approx(5)
    assert z.partial_at(variable_values, y) == approx(4)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(5)
    assert both_partials.partial_with_respect_to(y) == approx(4)
