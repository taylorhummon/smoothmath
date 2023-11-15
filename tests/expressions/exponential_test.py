from pytest import approx
import math
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Exponential

def test_exponential():
    x = Variable("x")
    z = Exponential(x)
    # at x = 0
    variable_values = VariableValues({x: 0})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(1)
    # at x = 1
    variable_values = VariableValues({x: 1})
    value = z.evaluate(variable_values)
    assert value == approx(math.e)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(math.e)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(math.e)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(math.e)
    # at x = -1
    variable_values = VariableValues({x: -1})
    value = z.evaluate(variable_values)
    assert value == approx(1 / math.e)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1 / math.e)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1 / math.e)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(1 / math.e)

def test_Exponential_composition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(6))
    variable_values = VariableValues({x: 3})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(2)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(2)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(2)

def test_base_two_Exponential():
    x = Variable("x")
    z = Exponential(x, 2)
    # at x = 0
    variable_values = VariableValues({x: 0})
    value = z.evaluate(variable_values)
    assert value == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0.693147180559)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0.693147180559)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(0.693147180559)
    # at x = 1
    variable_values = VariableValues({x: 1})
    value = z.evaluate(variable_values)
    assert value == approx(2)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1.386294361119)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1.386294361119)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(1.386294361119)
    # at x = -1
    variable_values = VariableValues({x: -1})
    value = z.evaluate(variable_values)
    assert value == approx(0.5)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0.346573590279)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0.346573590279)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(0.346573590279)

def test_base_two_Exponential_composition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(5), 2)
    variable_values = VariableValues({x: 3})
    value = z.evaluate(variable_values)
    assert value == approx(2)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(2.77258872223)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(2.77258872223)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(2.77258872223)
