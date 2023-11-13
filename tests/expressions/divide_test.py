from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions.constant import Constant
from smoothmath.expressions.variable import Variable
from smoothmath.expressions.logarithm import Logarithm
from smoothmath.expressions.divide import Divide

def testDivide():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    variable_values = VariableValues({ x: 5, y: 2 })
    value = z.evaluate(variable_values)
    assert value == approx(2.5)
    partial_with_respect_toX = z.partial_at(variable_values, x)
    assert partial_with_respect_toX == approx(0.5)
    partial_with_respect_toY = z.partial_at(variable_values, y)
    assert partial_with_respect_toY == approx(-1.25)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0.5)
    assert all_partials.partial_with_respect_to(y) == approx(-1.25)
    variable_values = VariableValues({ x: 3, y: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ x: 0, y: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def testDivideComposition():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    variable_values = VariableValues({ x: 3, y: 1 })
    value = z.evaluate(variable_values)
    assert value == approx(2)
    partial_with_respect_toX = z.partial_at(variable_values, x)
    assert partial_with_respect_toX == approx(0.4)
    partial_with_respect_toY = z.partial_at(variable_values, y)
    assert partial_with_respect_toY == approx(-2)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0.4)
    assert all_partials.partial_with_respect_to(y) == approx(-2)

def testDivideWithConstantNumeratorZero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    variable_values = VariableValues({ y: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)
    variable_values = VariableValues({ y: 0 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)

def testDivideWithConstantNumeratorZeroComposition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    variable_values = VariableValues({ y: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)

def testDivideWithConstantNumeratorZeroDoesntShortCircuit():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    variable_values = VariableValues({ y: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def testDivideWithConstantDenominatorOne():
    x = Variable("x")
    z = Divide(x, Constant(1))
    variable_values = VariableValues({ x: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(3)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)
    variable_values = VariableValues({ x: 0 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)

def testDivideWithConstantDenominatorZero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    variable_values = VariableValues({ x: 3 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ x: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
