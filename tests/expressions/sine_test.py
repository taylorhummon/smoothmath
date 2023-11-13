from pytest import approx
import math
from smoothmath.variable_values import VariableValues
from smoothmath.expressions.constant import Constant
from smoothmath.expressions.variable import Variable
from smoothmath.expressions.sine import Sine

def testSine():
    theta = Variable("theta")
    z = Sine(theta)
    variable_values = VariableValues({ theta: 0 })
    assert z.evaluate(variable_values) == approx(0)
    partial = z.partial_at(variable_values, theta)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(theta) == approx(1)
    variable_values = VariableValues({ theta: math.pi / 2 })
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, theta)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(theta) == approx(0)

def testSineComposition():
    theta = Variable("theta")
    z = Sine(Constant(2) * theta)
    variable_values = VariableValues({ theta: 0 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, theta)
    assert partial == approx(2)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(theta) == approx(2)
