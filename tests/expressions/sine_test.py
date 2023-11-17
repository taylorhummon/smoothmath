from pytest import approx
import math
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Sine


def test_Sine():
    theta = Variable("theta")
    z = Sine(theta)
    # at theta = 0
    variable_values = VariableValues({theta: 0})
    assert z.evaluate(variable_values) == approx(0)
    partial = z.partial_at(variable_values, theta)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(theta) == approx(1)
    # at theta = pi / 2
    variable_values = VariableValues({theta: math.pi / 2})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, theta)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(theta) == approx(0)


def test_Sine_composition():
    theta = Variable("theta")
    z = Sine(Constant(2) * theta)
    variable_values = VariableValues({theta: 0})
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, theta)
    assert partial == approx(2)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(theta) == approx(2)
