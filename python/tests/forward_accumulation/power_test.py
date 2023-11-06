from pytest import approx, raises
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.square_root import SquareRoot
from src.forward_accumulation.logarithm import Logarithm
from src.forward_accumulation.power import Power

def testPower():
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    variableValues = { x: 3, y: 2.5 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(15.588457268)
    assert resultForX.partial == approx(12.990381056)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(15.588457268)
    assert resultForY.partial == approx(17.125670716)
    variableValues = { x: 3, y: 0 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(1)
    assert resultForX.partial == approx(0)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(1)
    assert resultForY.partial == approx(1.0986122886)
    variableValues = { x: 3, y: -2.5 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(0.0641500299)
    assert resultForX.partial == approx(-0.0534583582)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(0.0641500299)
    assert resultForY.partial == approx(0.0704760111)
    variableValues = { x: 0, y: 2.5 }
    with raises(DomainException):
        z.derive(variableValues, x)
    with raises(DomainException):
        z.derive(variableValues, y)
    variableValues = { x: 0, y: 0 }
    with raises(DomainException):
        z.derive(variableValues, x)
    with raises(DomainException):
        z.derive(variableValues, y)
    variableValues = { x: 0, y: -2.5 }
    with raises(DomainException):
        z.derive(variableValues, x)
    with raises(DomainException):
        z.derive(variableValues, y)
    variableValues = { x: -3, y: 2.5 }
    with raises(DomainException):
        z.derive(variableValues, x)
    with raises(DomainException):
        z.derive(variableValues, y)
    variableValues = { x: -3, y: 0 }
    with raises(DomainException):
        z.derive(variableValues, x)
    with raises(DomainException):
        z.derive(variableValues, y)
    variableValues = { x: -3, y: -2.5 }
    with raises(DomainException):
        z.derive(variableValues, x)
    with raises(DomainException):
        z.derive(variableValues, y)

def testPowerComposition():
    x = Variable("x")
    y = Variable("y")
    z = Power(Constant(2) * x, Constant(3) * y)
    variableValues = { x: 1, y: 1 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(8)
    assert resultForX.partial == approx(24)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(8)
    assert resultForY.partial == approx(16.63553233343)

def testPowerWithConstantBaseOne():
    y = Variable("y")
    z = Power(Constant(1), y)
    result = z.derive({ y: 3 }, y)
    assert result.value == approx(1)
    assert result.partial == approx(0)
    result = z.derive({ y: 0 }, y)
    assert result.value == approx(1)
    assert result.partial == approx(0)
    result = z.derive({ y: -5 }, y)
    assert result.value == approx(1)
    assert result.partial == approx(0)

def testPowerWithConstantBaseOneDoesntShortCircuit():
    x = Variable("x")
    z = Power(Constant(1), SquareRoot(x))
    with raises(DomainException):
        z.derive({ x: -1 }, x)

def testPowerWithConstantBaseZero():
    y = Variable("y")
    z = Power(Constant(0), y)
    with raises(DomainException):
        z.derive({ y: 3 }, y)
    with raises(DomainException):
        z.derive({ y: 0 }, y)
    with raises(DomainException):
        z.derive({ y: -5 }, y)

def testPowerWithConstantBaseNegativeOne():
    y = Variable("y")
    z = Power(Constant(-1), y)
    with raises(DomainException):
        z.derive({ y: 3 }, y)
    with raises(DomainException):
        z.derive({ y: 0 }, y)
    with raises(DomainException):
        z.derive({ y: -5 }, y)

def testPowerWithConstantExponentTwo():
    x = Variable("x")
    z = Power(x, Constant(2))
    result = z.derive({ x: 3 }, x)
    assert result.value == approx(9)
    assert result.partial == approx(6)
    result = z.derive({ x: 0 }, x)
    assert result.value == approx(0)
    assert result.partial == approx(0)
    result = z.derive({ x: -5 }, x)
    assert result.value == approx(25)
    assert result.partial == approx(-10)

def testPowerWithConstantExponentTwoComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(2))
    result = z.derive({ x: 1 }, x)
    assert result.value == approx(4)
    assert result.partial == approx(12)

def testPowerWithConstantExponentOne():
    x = Variable("x")
    z = Power(x, Constant(1))
    result = z.derive({ x: 3 }, x)
    assert result.value == approx(3)
    assert result.partial == approx(1)
    result = z.derive({ x: 0 }, x)
    assert result.value == approx(0)
    assert result.partial == approx(1)
    result = z.derive({ x: -5 }, x)
    assert result.value == approx(-5)
    assert result.partial == approx(1)

def testPowerWithConstantExponentOneComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(1))
    result = z.derive({ x: 1 }, x)
    assert result.value == approx(2)
    assert result.partial == approx(3)

def testPowerWithConstantExponentZero():
    x = Variable("x")
    z = Power(x, Constant(0))
    result = z.derive({ x: 3 }, x)
    assert result.value == approx(1)
    assert result.partial == approx(0)
    result = z.derive({ x: 0 }, x)
    assert result.value == approx(1)
    assert result.partial == approx(0)
    result = z.derive({ x: -5 }, x)
    assert result.value == approx(1)
    assert result.partial == approx(0)

def testPowerWithConstantExponentZeroComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(0))
    result = z.derive({ x: 1 }, x)
    assert result.value == approx(1)
    assert result.partial == approx(0)

def testPowerWithConstantExponentZeroDoesntShortCircuit():
    x = Variable("x")
    z = Power(Logarithm(x), Constant(0))
    with raises(DomainException):
        z.derive({ x: 0 }, x)

def testPowerWithConstantExponentNegativeOne():
    x = Variable("x")
    z = Power(x, Constant(-1))
    result = z.derive({ x: 2 }, x)
    assert result.value == approx(0.5)
    assert result.partial == approx(-0.25)
    with raises(DomainException):
        z.derive({ x: 0 }, x)
    result = z.derive({ x: -5 }, x)
    assert result.value == approx(-0.2)
    assert result.partial == approx(-0.04)

def testPowerWithConstantExponentNegativeOneComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-1))
    result = z.derive({ x: 1 }, x)
    assert result.value == approx(0.5)
    assert result.partial == approx(-0.75)

def testPowerWithConstantExponentNegativeTwo():
    x = Variable("x")
    z = Power(x, Constant(-2))
    result = z.derive({ x: 2 }, x)
    assert result.value == approx(0.25)
    assert result.partial == approx(-0.25)
    with raises(DomainException):
        z.derive({ x: 0 }, x)
    result = z.derive({ x: -5 }, x)
    assert result.value == approx(0.04)
    assert result.partial == approx(0.016)

def testPowerWithConstantExponentNegativeTwoComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-2))
    result = z.derive({ x: 1 }, x)
    assert result.value == approx(0.25)
    assert result.partial == approx(-0.75)

def testPowerWithExponentMadeFromAddingConstants():
    x = Variable("x")
    z = Power(x, Constant(1) + Constant(1))
    result = z.derive({ x: 3 }, x)
    assert result.value == approx(9)
    assert result.partial == approx(6)
    result = z.derive({ x: 0 }, x)
    assert result.value == approx(0)
    assert result.partial == approx(0)
    result = z.derive({ x: -5 }, x)
    assert result.value == approx(25)
    assert result.partial == approx(-10)

def testPowerWhereExponentIsAnIntegerRepresentedAsAFloat():
    x = Variable("x")
    z = Power(x, Constant(2.0))
    result = z.derive({ x: -5 }, x)
    assert result.value == approx(25)
    assert result.partial == approx(-10)
