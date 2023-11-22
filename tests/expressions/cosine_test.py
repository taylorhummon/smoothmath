from pytest import approx
import math
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Cosine


def test_Cosine():
    theta = Variable("theta")
    z = Cosine(theta)
    # at theta = 0
    variable_values = VariableValues({theta: 0})
    assert z.evaluate(variable_values) == approx(1)
    assert z.partial_at(variable_values, theta) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(theta) == approx(0)
    assert z.synthetic_partial(theta).evaluate(variable_values) == approx(0)
    # theta = pi / 2
    variable_values = VariableValues({theta: math.pi / 2})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, theta) == approx(-1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(theta) == approx(-1)
    assert z.synthetic_partial(theta).evaluate(variable_values) == approx(-1)


def test_Cosine_composition():
    theta = Variable("theta")
    z = Cosine(Constant(2) * theta)
    variable_values = VariableValues({theta: math.pi / 4})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, theta) == approx(-2)
    assert z.all_partials_at(variable_values).partial_with_respect_to(theta) == approx(-2)
    assert z.synthetic_partial(theta).evaluate(variable_values) == approx(-2)
