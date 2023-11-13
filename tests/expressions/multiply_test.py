from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions.constant import Constant
from smoothmath.expressions.variable import Variable
from smoothmath.expressions.multiply import Multiply
from smoothmath.expressions.power import Power

def testMultiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    variable_values = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(6)
    partial_with_respect_toX = z.partial_at(variable_values, x)
    assert partial_with_respect_toX == approx(3)
    partial_with_respect_toY = z.partial_at(variable_values, y)
    assert partial_with_respect_toY == approx(2)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(3)
    assert all_partials.partial_with_respect_to(y) == approx(2)

def testMultiplyComposition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    variable_values = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(20)
    partial_with_respect_toX = z.partial_at(variable_values, x)
    assert partial_with_respect_toX == approx(10)
    partial_with_respect_toY = z.partial_at(variable_values, y)
    assert partial_with_respect_toY == approx(10)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(10)
    assert all_partials.partial_with_respect_to(y) == approx(10)

def testMultiplyByZero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    variable_values = VariableValues({ x: 2 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)

def testMultiplyByZeroDoesntShortCircuit():
    x = Variable("x")
    z = Multiply(Constant(0), Power(Constant(-1), x))
    variable_values = VariableValues({ x: 2 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def testMultiplyByOne():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    variable_values = VariableValues({ x: 2 })
    value = z.evaluate(variable_values)
    assert value == approx(2)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)
