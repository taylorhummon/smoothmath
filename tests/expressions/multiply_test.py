from pytest import approx
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Multiply


def test_Multiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    variable_values = VariableValues({x: 2, y: 3})
    assert z.evaluate(variable_values) == approx(6)
    assert z.partial_at(variable_values, x) == approx(3)
    assert z.partial_at(variable_values, y) == approx(2)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(3)
    assert both_partials.partial_with_respect_to(y) == approx(2)
    synthetic = z.synthetic()
    assert synthetic.partial_at(variable_values, x) == approx(3)
    assert synthetic.partial_at(variable_values, y) == approx(2)


def test_Multiply_composition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    variable_values = VariableValues({x: 2, y: 3})
    assert z.evaluate(variable_values) == approx(20)
    assert z.partial_at(variable_values, x) == approx(10)
    assert z.partial_at(variable_values, y) == approx(10)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(10)
    assert both_partials.partial_with_respect_to(y) == approx(10)
    synthetic = z.synthetic()
    assert synthetic.partial_at(variable_values, x) == approx(10)
    assert synthetic.partial_at(variable_values, y) == approx(10)


def test_Multiply_by_zero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(0)
    assert z.partial_at(variable_values, x) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(0)
    assert z.synthetic().partial_at(variable_values, x) == approx(0)


def test_Multiply_by_one():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(2)
    assert z.partial_at(variable_values, x) == approx(1)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(1)
    assert z.synthetic().partial_at(variable_values, x) == approx(1)
