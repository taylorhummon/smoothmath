from pytest import approx, raises
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.square_root import SquareRoot
from src.smooth_expression.logarithm import Logarithm
from src.smooth_expression.power import Power

def testPower():
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    variableValues = { x: 3, y: 2.5 }
    singleResultForX = z.deriveSingle(variableValues, x)
    assert singleResultForX.value == approx(15.588457268)
    assert singleResultForX.partial == approx(12.990381056)
    singleResultForY = z.deriveSingle(variableValues, y)
    assert singleResultForY.value == approx(15.588457268)
    assert singleResultForY.partial == approx(17.125670716)
    variableValues = { x: 3, y: 0 }
    singleResultForX = z.deriveSingle(variableValues, x)
    assert singleResultForX.value == approx(1)
    assert singleResultForX.partial == approx(0)
    singleResultForY = z.deriveSingle(variableValues, y)
    assert singleResultForY.value == approx(1)
    assert singleResultForY.partial == approx(1.0986122886)
    variableValues = { x: 3, y: -2.5 }
    singleResultForX = z.deriveSingle(variableValues, x)
    assert singleResultForX.value == approx(0.0641500299)
    assert singleResultForX.partial == approx(-0.0534583582)
    singleResultForY = z.deriveSingle(variableValues, y)
    assert singleResultForY.value == approx(0.0641500299)
    assert singleResultForY.partial == approx(0.0704760111)
    variableValues = { x: 0, y: 2.5 }
    with raises(DomainException):
        z.deriveSingle(variableValues, x)
    with raises(DomainException):
        z.deriveSingle(variableValues, y)
    variableValues = { x: 0, y: 0 }
    with raises(DomainException):
        z.deriveSingle(variableValues, x)
    with raises(DomainException):
        z.deriveSingle(variableValues, y)
    variableValues = { x: 0, y: -2.5 }
    with raises(DomainException):
        z.deriveSingle(variableValues, x)
    with raises(DomainException):
        z.deriveSingle(variableValues, y)
    variableValues = { x: -3, y: 2.5 }
    with raises(DomainException):
        z.deriveSingle(variableValues, x)
    with raises(DomainException):
        z.deriveSingle(variableValues, y)
    variableValues = { x: -3, y: 0 }
    with raises(DomainException):
        z.deriveSingle(variableValues, x)
    with raises(DomainException):
        z.deriveSingle(variableValues, y)
    variableValues = { x: -3, y: -2.5 }
    with raises(DomainException):
        z.deriveSingle(variableValues, x)
    with raises(DomainException):
        z.deriveSingle(variableValues, y)

def testPowerComposition():
    x = Variable("x")
    y = Variable("y")
    z = Power(Constant(2) * x, Constant(3) * y)
    variableValues = { x: 1, y: 1 }
    singleResultForX = z.deriveSingle(variableValues, x)
    assert singleResultForX.value == approx(8)
    assert singleResultForX.partial == approx(24)
    singleResultForY = z.deriveSingle(variableValues, y)
    assert singleResultForY.value == approx(8)
    assert singleResultForY.partial == approx(16.63553233343)

def testPowerWithConstantBaseOne():
    y = Variable("y")
    z = Power(Constant(1), y)
    singleResult = z.deriveSingle({ y: 3 }, y)
    assert singleResult.value == approx(1)
    assert singleResult.partial == approx(0)
    singleResult = z.deriveSingle({ y: 0 }, y)
    assert singleResult.value == approx(1)
    assert singleResult.partial == approx(0)
    singleResult = z.deriveSingle({ y: -5 }, y)
    assert singleResult.value == approx(1)
    assert singleResult.partial == approx(0)

def testPowerWithConstantBaseOneDoesntShortCircuit():
    x = Variable("x")
    z = Power(Constant(1), SquareRoot(x))
    with raises(DomainException):
        z.deriveSingle({ x: -1 }, x)

def testPowerWithConstantBaseZero():
    y = Variable("y")
    z = Power(Constant(0), y)
    with raises(DomainException):
        z.deriveSingle({ y: 3 }, y)
    with raises(DomainException):
        z.deriveSingle({ y: 0 }, y)
    with raises(DomainException):
        z.deriveSingle({ y: -5 }, y)

def testPowerWithConstantBaseNegativeOne():
    y = Variable("y")
    z = Power(Constant(-1), y)
    with raises(DomainException):
        z.deriveSingle({ y: 3 }, y)
    with raises(DomainException):
        z.deriveSingle({ y: 0 }, y)
    with raises(DomainException):
        z.deriveSingle({ y: -5 }, y)

def testPowerWithConstantExponentTwo():
    x = Variable("x")
    z = Power(x, Constant(2))
    singleResult = z.deriveSingle({ x: 3 }, x)
    assert singleResult.value == approx(9)
    assert singleResult.partial == approx(6)
    singleResult = z.deriveSingle({ x: 0 }, x)
    assert singleResult.value == approx(0)
    assert singleResult.partial == approx(0)
    singleResult = z.deriveSingle({ x: -5 }, x)
    assert singleResult.value == approx(25)
    assert singleResult.partial == approx(-10)

def testPowerWithConstantExponentTwoComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(2))
    singleResult = z.deriveSingle({ x: 1 }, x)
    assert singleResult.value == approx(4)
    assert singleResult.partial == approx(12)

def testPowerWithConstantExponentOne():
    x = Variable("x")
    z = Power(x, Constant(1))
    singleResult = z.deriveSingle({ x: 3 }, x)
    assert singleResult.value == approx(3)
    assert singleResult.partial == approx(1)
    singleResult = z.deriveSingle({ x: 0 }, x)
    assert singleResult.value == approx(0)
    assert singleResult.partial == approx(1)
    singleResult = z.deriveSingle({ x: -5 }, x)
    assert singleResult.value == approx(-5)
    assert singleResult.partial == approx(1)

def testPowerWithConstantExponentOneComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(1))
    singleResult = z.deriveSingle({ x: 1 }, x)
    assert singleResult.value == approx(2)
    assert singleResult.partial == approx(3)

def testPowerWithConstantExponentZero():
    x = Variable("x")
    z = Power(x, Constant(0))
    singleResult = z.deriveSingle({ x: 3 }, x)
    assert singleResult.value == approx(1)
    assert singleResult.partial == approx(0)
    singleResult = z.deriveSingle({ x: 0 }, x)
    assert singleResult.value == approx(1)
    assert singleResult.partial == approx(0)
    singleResult = z.deriveSingle({ x: -5 }, x)
    assert singleResult.value == approx(1)
    assert singleResult.partial == approx(0)

def testPowerWithConstantExponentZeroComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(0))
    singleResult = z.deriveSingle({ x: 1 }, x)
    assert singleResult.value == approx(1)
    assert singleResult.partial == approx(0)

def testPowerWithConstantExponentZeroDoesntShortCircuit():
    x = Variable("x")
    z = Power(Logarithm(x), Constant(0))
    with raises(DomainException):
        z.deriveSingle({ x: 0 }, x)

def testPowerWithConstantExponentNegativeOne():
    x = Variable("x")
    z = Power(x, Constant(-1))
    singleResult = z.deriveSingle({ x: 2 }, x)
    assert singleResult.value == approx(0.5)
    assert singleResult.partial == approx(-0.25)
    with raises(DomainException):
        z.deriveSingle({ x: 0 }, x)
    singleResult = z.deriveSingle({ x: -5 }, x)
    assert singleResult.value == approx(-0.2)
    assert singleResult.partial == approx(-0.04)

def testPowerWithConstantExponentNegativeOneComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-1))
    singleResult = z.deriveSingle({ x: 1 }, x)
    assert singleResult.value == approx(0.5)
    assert singleResult.partial == approx(-0.75)

def testPowerWithConstantExponentNegativeTwo():
    x = Variable("x")
    z = Power(x, Constant(-2))
    singleResult = z.deriveSingle({ x: 2 }, x)
    assert singleResult.value == approx(0.25)
    assert singleResult.partial == approx(-0.25)
    with raises(DomainException):
        z.deriveSingle({ x: 0 }, x)
    singleResult = z.deriveSingle({ x: -5 }, x)
    assert singleResult.value == approx(0.04)
    assert singleResult.partial == approx(0.016)

def testPowerWithConstantExponentNegativeTwoComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-2))
    singleResult = z.deriveSingle({ x: 1 }, x)
    assert singleResult.value == approx(0.25)
    assert singleResult.partial == approx(-0.75)

def testPowerWithExponentMadeFromAddingConstants():
    x = Variable("x")
    z = Power(x, Constant(1) + Constant(1))
    singleResult = z.deriveSingle({ x: 3 }, x)
    assert singleResult.value == approx(9)
    assert singleResult.partial == approx(6)
    singleResult = z.deriveSingle({ x: 0 }, x)
    assert singleResult.value == approx(0)
    assert singleResult.partial == approx(0)
    singleResult = z.deriveSingle({ x: -5 }, x)
    assert singleResult.value == approx(25)
    assert singleResult.partial == approx(-10)

def testPowerWhereExponentIsAnIntegerRepresentedAsAFloat():
    x = Variable("x")
    z = Power(x, Constant(2.0))
    singleResult = z.deriveSingle({ x: -5 }, x)
    assert singleResult.value == approx(25)
    assert singleResult.partial == approx(-10)

def testPowerMulti():
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    multiResult = z.deriveMulti({ x: 3, y: 2.5 })
    assert multiResult.value == approx(15.588457268)
    assert multiResult.partialWithRespectTo(x) == approx(12.990381056)
    assert multiResult.partialWithRespectTo(y) == approx(17.125670716)
    multiResult = z.deriveMulti({ x: 3, y: 0 })
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(x) == approx(0)
    assert multiResult.partialWithRespectTo(y) == approx(1.0986122886)
    multiResult = z.deriveMulti({ x: 3, y: -2.5 })
    assert multiResult.value == approx(0.0641500299)
    assert multiResult.partialWithRespectTo(x) == approx(-0.0534583582)
    assert multiResult.partialWithRespectTo(y) == approx(0.0704760111)
    with raises(DomainException):
        z.deriveMulti({ x: 0, y: 2.5 })
    with raises(DomainException):
        z.deriveMulti({ x: 0, y: 0 })
    with raises(DomainException):
        z.deriveMulti({ x: 0, y: -2.5 })
    with raises(DomainException):
        z.deriveMulti({ x: -3, y: 2.5 })
    with raises(DomainException):
        z.deriveMulti({ x: -3, y: 0 })
    with raises(DomainException):
        z.deriveMulti({ x: -3, y: -2.5 })

def testPowerCompositionMulti():
    x = Variable("x")
    y = Variable("y")
    z = Power(Constant(2) * x, Constant(3) * y)
    multiResult = z.deriveMulti({ x: 1, y: 1 })
    assert multiResult.value == approx(8)
    assert multiResult.partialWithRespectTo(x) == approx(24)
    assert multiResult.partialWithRespectTo(y) == approx(16.63553233343)

def testPowerWithConstantBaseOneMulti():
    y = Variable("y")
    z = Power(Constant(1), y)
    multiResult = z.deriveMulti({ y: 3 })
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(y) == approx(0)
    multiResult = z.deriveMulti({ y: 0 })
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(y) == approx(0)
    multiResult = z.deriveMulti({ y: -5 })
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(y) == approx(0)

def testPowerWithConstantBaseOneDoesntShortCircuitMulti():
    x = Variable("x")
    z = Power(Constant(1), SquareRoot(x))
    with raises(DomainException):
        z.deriveMulti({ x: -1 })

def testPowerWithConstantBaseZeroMulti():
    y = Variable("y")
    z = Power(Constant(0), y)
    with raises(DomainException):
        z.deriveMulti({ y: 3 })
    with raises(DomainException):
        z.deriveMulti({ y: 0 })
    with raises(DomainException):
        z.deriveMulti({ y: -5 })

def testPowerWithConstantBaseNegativeOneMulti():
    y = Variable("y")
    z = Power(Constant(-1), y)
    with raises(DomainException):
        z.deriveMulti({ y: 3 })
    with raises(DomainException):
        z.deriveMulti({ y: 0 })
    with raises(DomainException):
        z.deriveMulti({ y: -5 })

def testPowerWithConstantExponentTwoMulti():
    x = Variable("x")
    z = Power(x, Constant(2))
    multiResult = z.deriveMulti({ x: 3 })
    assert multiResult.value == approx(9)
    assert multiResult.partialWithRespectTo(x) == approx(6)
    multiResult = z.deriveMulti({ x: 0 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(x) == approx(0)
    multiResult = z.deriveMulti({ x: -5 })
    assert multiResult.value == approx(25)
    assert multiResult.partialWithRespectTo(x) == approx(-10)

def testPowerWithConstantExponentTwoCompositionMulti():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(2))
    multiResult = z.deriveMulti({ x: 1 })
    assert multiResult.value == approx(4)
    assert multiResult.partialWithRespectTo(x) == approx(12)

def testPowerWithConstantExponentOneMulti():
    x = Variable("x")
    z = Power(x, Constant(1))
    multiResult = z.deriveMulti({ x: 3 })
    assert multiResult.value == approx(3)
    assert multiResult.partialWithRespectTo(x) == approx(1)
    multiResult = z.deriveMulti({ x: 0 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(x) == approx(1)
    multiResult = z.deriveMulti({ x: -5 })
    assert multiResult.value == approx(-5)
    assert multiResult.partialWithRespectTo(x) == approx(1)

def testPowerWithConstantExponentOneCompositionMulti():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(1))
    multiResult = z.deriveMulti({ x: 1 })
    assert multiResult.value == approx(2)
    assert multiResult.partialWithRespectTo(x) == approx(3)

def testPowerWithConstantExponentZeroMulti():
    x = Variable("x")
    z = Power(x, Constant(0))
    multiResult = z.deriveMulti({ x: 3 })
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(x) == approx(0)
    multiResult = z.deriveMulti({ x: 0 })
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(x) == approx(0)
    multiResult = z.deriveMulti({ x: -5 })
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(x) == approx(0)

def testPowerWithConstantExponentZeroCompositionMulti():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(0))
    multiResult = z.deriveMulti({ x: 1 })
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(x) == approx(0)

def testPowerWithConstantExponentZeroDoesntShortCircuitMulti():
    x = Variable("x")
    z = Power(Logarithm(x), Constant(0))
    with raises(DomainException):
        z.deriveMulti({ x: 0 })

def testPowerWithConstantExponentNegativeOneMulti():
    x = Variable("x")
    z = Power(x, Constant(-1))
    multiResult = z.deriveMulti({ x: 2 })
    assert multiResult.value == approx(0.5)
    assert multiResult.partialWithRespectTo(x) == approx(-0.25)
    with raises(DomainException):
        z.deriveMulti({ x: 0 })
    multiResult = z.deriveMulti({ x: -5 })
    assert multiResult.value == approx(-0.2)
    assert multiResult.partialWithRespectTo(x) == approx(-0.04)

def testPowerWithConstantExponentNegativeOneCompositionMulti():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-1))
    multiResult = z.deriveMulti({ x: 1 })
    assert multiResult.value == approx(0.5)
    assert multiResult.partialWithRespectTo(x) == approx(-0.75)

def testPowerWithConstantExponentNegativeTwoMulti():
    x = Variable("x")
    z = Power(x, Constant(-2))
    multiResult = z.deriveMulti({ x: 2 })
    assert multiResult.value == approx(0.25)
    assert multiResult.partialWithRespectTo(x) == approx(-0.25)
    with raises(DomainException):
        z.deriveMulti({ x: 0 })
    multiResult = z.deriveMulti({ x: -5 })
    assert multiResult.value == approx(0.04)
    assert multiResult.partialWithRespectTo(x) == approx(0.016)

def testPowerWithConstantExponentNegativeTwoCompositionMulti():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-2))
    multiResult = z.deriveMulti({ x: 1 })
    assert multiResult.value == approx(0.25)
    assert multiResult.partialWithRespectTo(x) == approx(-0.75)

def testPowerWithExponentMadeFromAddingConstantsMulti():
    x = Variable("x")
    z = Power(x, Constant(1) + Constant(1))
    multiResult = z.deriveMulti({ x: 3 })
    assert multiResult.value == approx(9)
    assert multiResult.partialWithRespectTo(x) == approx(6)
    multiResult = z.deriveMulti({ x: 0 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(x) == approx(0)
    multiResult = z.deriveMulti({ x: -5 })
    assert multiResult.value == approx(25)
    assert multiResult.partialWithRespectTo(x) == approx(-10)

def testPowerWhereExponentIsAnIntegerRepresentedAsAFloatMulti():
    x = Variable("x")
    z = Power(x, Constant(2.0))
    multiResult = z.deriveMulti({ x: -5 })
    assert multiResult.value == approx(25)
    assert multiResult.partialWithRespectTo(x) == approx(-10)
