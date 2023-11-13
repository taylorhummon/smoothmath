from pytest import approx, raises
from smoothmath.variable_values import VariableValues
from smoothmath.errors import DomainError
from smoothmath.expressions.constant import Constant
from smoothmath.expressions.variable import Variable
from smoothmath.expressions.square_root import SquareRoot
from smoothmath.expressions.logarithm import Logarithm
from smoothmath.expressions.power import Power

def testPower():
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    variable_values = VariableValues({ x: 3, y: 2.5 })
    value = z.evaluate(variable_values)
    assert value == approx(15.588457268)
    partial_with_respect_toX = z.partial_at(variable_values, x)
    assert partial_with_respect_toX == approx(12.990381056)
    partial_with_respect_toY = z.partial_at(variable_values, y)
    assert partial_with_respect_toY == approx(17.125670716)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(12.990381056)
    assert all_partials.partial_with_respect_to(y) == approx(17.125670716)
    variable_values = VariableValues({ x: 3, y: 0 })
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial_with_respect_toX = z.partial_at(variable_values, x)
    assert partial_with_respect_toX == approx(0)
    partial_with_respect_toY = z.partial_at(variable_values, y)
    assert partial_with_respect_toY == approx(1.0986122886)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)
    assert all_partials.partial_with_respect_to(y) == approx(1.0986122886)
    variable_values = VariableValues({ x: 3, y: -2.5 })
    value = z.evaluate(variable_values)
    assert value == approx(0.0641500299)
    partial_with_respect_toX = z.partial_at(variable_values, x)
    assert partial_with_respect_toX == approx(-0.0534583582)
    partial_with_respect_toY = z.partial_at(variable_values, y)
    assert partial_with_respect_toY == approx(0.0704760111)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.0534583582)
    assert all_partials.partial_with_respect_to(y) == approx(0.0704760111)
    variable_values = VariableValues({ x: 0, y: 2.5 })
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
    variable_values = VariableValues({ x: 0, y: -2.5 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ x: -3, y: 2.5 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ x: -3, y: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ x: -3, y: -2.5 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def testPowerComposition():
    x = Variable("x")
    y = Variable("y")
    z = Power(Constant(2) * x, Constant(3) * y)
    variable_values = VariableValues({ x: 1, y: 1 })
    value = z.evaluate(variable_values)
    assert value == approx(8)
    partial_with_respect_toX = z.partial_at(variable_values, x)
    assert partial_with_respect_toX == approx(24)
    partial_with_respect_toY = z.partial_at(variable_values, y)
    assert partial_with_respect_toY == approx(16.63553233343)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(24)
    assert all_partials.partial_with_respect_to(y) == approx(16.63553233343)

def testPowerWithConstantBaseOne():
    y = Variable("y")
    z = Power(Constant(1), y)
    variable_values = VariableValues({ y: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)
    variable_values = VariableValues({ y: 0 })
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)
    variable_values = VariableValues({ y: -5 })
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, y)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == approx(0)

def testPowerWithConstantBaseOneDoesntShortCircuit():
    x = Variable("x")
    z = Power(Constant(1), SquareRoot(x))
    variable_values = VariableValues({ x: -1 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def testPowerWithConstantBaseZero():
    y = Variable("y")
    z = Power(Constant(0), y)
    variable_values = VariableValues({ y: 3 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ y: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ y: -5 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def testPowerWithConstantBaseNegativeOne():
    y = Variable("y")
    z = Power(Constant(-1), y)
    variable_values = VariableValues({ y: 3 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ y: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ y: -5 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, y)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def testPowerWithConstantExponentTwo():
    x = Variable("x")
    z = Power(x, Constant(2))
    variable_values = VariableValues({ x: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(9)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(6)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(6)
    variable_values = VariableValues({ x: 0 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)
    variable_values = VariableValues({ x: -5 })
    value = z.evaluate(variable_values)
    assert value == approx(25)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-10)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-10)

def testPowerWithConstantExponentTwoComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(2))
    variable_values = VariableValues({ x: 1 })
    value = z.evaluate(variable_values)
    assert value == approx(4)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(12)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(12)

def testPowerWithConstantExponentOne():
    x = Variable("x")
    z = Power(x, Constant(1))
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
    variable_values = VariableValues({ x: -5 })
    value = z.evaluate(variable_values)
    assert value == approx(-5)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(1)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(1)

def testPowerWithConstantExponentOneComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(1))
    variable_values = VariableValues({ x: 1 })
    value = z.evaluate(variable_values)
    assert value == approx(2)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(3)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(3)

def testPowerWithConstantExponentZero():
    x = Variable("x")
    z = Power(x, Constant(0))
    variable_values = VariableValues({ x: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)
    variable_values = VariableValues({ x: 0 })
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)
    variable_values = VariableValues({ x: -5 })
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)

def testPowerWithConstantExponentZeroComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(0))
    variable_values = VariableValues({ x: 1 })
    value = z.evaluate(variable_values)
    assert value == approx(1)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)

def testPowerWithConstantExponentZeroDoesntShortCircuit():
    x = Variable("x")
    z = Power(Logarithm(x), Constant(0))
    variable_values = VariableValues({ x: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def testPowerWithConstantExponentNegativeOne():
    x = Variable("x")
    z = Power(x, Constant(-1))
    variable_values = VariableValues({ x: 2 })
    value = z.evaluate(variable_values)
    assert value == approx(0.5)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-0.25)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.25)
    variable_values = VariableValues({ x: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ x: -5 })
    value = z.evaluate(variable_values)
    assert value == approx(-0.2)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-0.04)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.04)

def testPowerWithConstantExponentNegativeOneComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-1))
    variable_values = VariableValues({ x: 1 })
    value = z.evaluate(variable_values)
    assert value == approx(0.5)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-0.75)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.75)

def testPowerWithConstantExponentNegativeTwo():
    x = Variable("x")
    z = Power(x, Constant(-2))
    variable_values = VariableValues({ x: 2 })
    value = z.evaluate(variable_values)
    assert value == approx(0.25)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-0.25)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.25)
    variable_values = VariableValues({ x: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, x)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    variable_values = VariableValues({ x: -5 })
    value = z.evaluate(variable_values)
    assert value == approx(0.04)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0.016)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0.016)

def testPowerWithConstantExponentNegativeTwoComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-2))
    variable_values = VariableValues({ x: 1 })
    value = z.evaluate(variable_values)
    assert value == approx(0.25)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-0.75)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.75)

def testPowerWithExponentMadeFromAddingConstants():
    x = Variable("x")
    z = Power(x, Constant(1) + Constant(1))
    variable_values = VariableValues({ x: 3 })
    value = z.evaluate(variable_values)
    assert value == approx(9)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(6)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(6)
    variable_values = VariableValues({ x: 0 })
    value = z.evaluate(variable_values)
    assert value == approx(0)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(0)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(0)
    variable_values = VariableValues({ x: -5 })
    value = z.evaluate(variable_values)
    assert value == approx(25)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-10)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-10)

def testPowerWhereExponentIsAnIntegerRepresentedAsAFloat():
    x = Variable("x")
    z = Power(x, Constant(2.0))
    variable_values = VariableValues({ x: -5 })
    value = z.evaluate(variable_values)
    assert value == approx(25)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-10)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-10)
