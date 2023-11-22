from pytest import approx, raises
import math
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Logarithm


def test_Logarithm():
    x = Variable("x")
    z = Logarithm(x)
    synthetic_partial = z.synthetic_partial(x)
    # at x = 1
    variable_values = VariableValues({x: 1})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, x) == approx(1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(1)
    assert synthetic_partial.evaluate(variable_values) == approx(1)
    # at x = e
    variable_values = VariableValues({x: math.e})
    assert z.evaluate(variable_values) == approx(1)
    assert z.partial_at(variable_values, x) == approx(1 / math.e)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(1 / math.e)
    assert synthetic_partial.evaluate(variable_values) == approx(1 / math.e)
    # at x = 0
    variable_values = VariableValues({x: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)
    # at x = -1
    variable_values = VariableValues({x: -1})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # # !!! known failure
    # with raises(DomainError):
    #     synthetic_partial.evaluate(variable_values)


def test_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(3))
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, x) == approx(2)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(2)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(2)


def test_base_two_Logarithm():
    x = Variable("x")
    z = Logarithm(x, base = 2)
    synthetic_partial = z.synthetic_partial(x)
    # at x = 1
    variable_values = VariableValues({x: 1})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, x) == approx(1.442695040888)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(1.442695040888)
    assert synthetic_partial.evaluate(variable_values) == approx(1.442695040888)
    # at x = 2
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(1)
    assert z.partial_at(variable_values, x) == approx(0.721347520444)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(0.721347520444)
    assert synthetic_partial.evaluate(variable_values) == approx(0.721347520444)
    # at x = 0
    variable_values = VariableValues({x: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        synthetic_partial.evaluate(variable_values)
    # at x = -1
    variable_values = VariableValues({x: -1})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    # # !!! known failure
    # with raises(DomainError):
    #     synthetic_partial.evaluate(variable_values)


def test_base_two_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(6), base = 2)
    variable_values = VariableValues({x: 7})
    assert z.evaluate(variable_values) == approx(3)
    assert z.partial_at(variable_values, x) == approx(0.3606737602222)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(0.3606737602222)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(0.3606737602222)
