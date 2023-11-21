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
    assert z.partial_at(variable_values, theta) == approx(1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(theta) == approx(1)
    # at theta = pi / 2
    variable_values = VariableValues({theta: math.pi / 2})
    assert z.evaluate(variable_values) == approx(1)
    assert z.partial_at(variable_values, theta) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(theta) == approx(0)


def test_Sine_composition():
    theta = Variable("theta")
    z = Sine(Constant(2) * theta)
    variable_values = VariableValues({theta: 0})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, theta) == approx(2)
    assert z.all_partials_at(variable_values).partial_with_respect_to(theta) == approx(2)
