from pytest import approx
import math
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Cosine

def test_Cosine():
    theta = Variable("theta")
    z = Cosine(theta)
    variable_values = VariableValues({theta: 0})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, theta)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(theta) == approx(0)
    variable_values = VariableValues({theta: math.pi / 2})
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, theta)
    assert partial == approx(-1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(theta) == approx(-1)

def test_Cosine_composition():
    theta = Variable("theta")
    z = Cosine(Constant(2) * theta)
    variable_values = VariableValues({theta: math.pi / 4})
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, theta)
    assert partial == approx(-2)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(theta) == approx(-2)
