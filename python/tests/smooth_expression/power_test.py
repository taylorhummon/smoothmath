from pytest import approx, raises
from src.smooth_expression.variable_values import VariableValues
from src.smooth_expression.custom_exceptions import DomainError
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.square_root import SquareRoot
from src.smooth_expression.logarithm import Logarithm
from src.smooth_expression.power import Power

def testPower():
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    variableValues = VariableValues({ x: 3, y: 2.5 })
    value = z.evaluate(variableValues)
    assert value == approx(15.588457268)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(12.990381056)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(17.125670716)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(12.990381056)
    assert allPartials.partialWithRespectTo(y) == approx(17.125670716)
    variableValues = VariableValues({ x: 3, y: 0 })
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(0)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(1.0986122886)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0)
    assert allPartials.partialWithRespectTo(y) == approx(1.0986122886)
    variableValues = VariableValues({ x: 3, y: -2.5 })
    value = z.evaluate(variableValues)
    assert value == approx(0.0641500299)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(-0.0534583582)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(0.0704760111)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-0.0534583582)
    assert allPartials.partialWithRespectTo(y) == approx(0.0704760111)
    variableValues = VariableValues({ x: 0, y: 2.5 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ x: 0, y: 0 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ x: 0, y: -2.5 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ x: -3, y: 2.5 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ x: -3, y: 0 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ x: -3, y: -2.5 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)

def testPowerComposition():
    x = Variable("x")
    y = Variable("y")
    z = Power(Constant(2) * x, Constant(3) * y)
    variableValues = VariableValues({ x: 1, y: 1 })
    value = z.evaluate(variableValues)
    assert value == approx(8)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(24)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(16.63553233343)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(24)
    assert allPartials.partialWithRespectTo(y) == approx(16.63553233343)

def testPowerWithConstantBaseOne():
    y = Variable("y")
    z = Power(Constant(1), y)
    variableValues = VariableValues({ y: 3 })
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, y)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(y) == approx(0)
    variableValues = VariableValues({ y: 0 })
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, y)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(y) == approx(0)
    variableValues = VariableValues({ y: -5 })
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, y)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(y) == approx(0)

def testPowerWithConstantBaseOneDoesntShortCircuit():
    x = Variable("x")
    z = Power(Constant(1), SquareRoot(x))
    variableValues = VariableValues({ x: -1 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.allPartialsAt(variableValues)

def testPowerWithConstantBaseZero():
    y = Variable("y")
    z = Power(Constant(0), y)
    variableValues = VariableValues({ y: 3 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ y: 0 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ y: -5 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)

def testPowerWithConstantBaseNegativeOne():
    y = Variable("y")
    z = Power(Constant(-1), y)
    variableValues = VariableValues({ y: 3 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ y: 0 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ y: -5 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, y)
    with raises(DomainError):
        z.allPartialsAt(variableValues)

def testPowerWithConstantExponentTwo():
    x = Variable("x")
    z = Power(x, Constant(2))
    variableValues = VariableValues({ x: 3 })
    value = z.evaluate(variableValues)
    assert value == approx(9)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(6)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(6)
    variableValues = VariableValues({ x: 0 })
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0)
    variableValues = VariableValues({ x: -5 })
    value = z.evaluate(variableValues)
    assert value == approx(25)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(-10)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-10)

def testPowerWithConstantExponentTwoComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(2))
    variableValues = VariableValues({ x: 1 })
    value = z.evaluate(variableValues)
    assert value == approx(4)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(12)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(12)

def testPowerWithConstantExponentOne():
    x = Variable("x")
    z = Power(x, Constant(1))
    variableValues = VariableValues({ x: 3 })
    value = z.evaluate(variableValues)
    assert value == approx(3)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1)
    variableValues = VariableValues({ x: 0 })
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1)
    variableValues = VariableValues({ x: -5 })
    value = z.evaluate(variableValues)
    assert value == approx(-5)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1)

def testPowerWithConstantExponentOneComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(1))
    variableValues = VariableValues({ x: 1 })
    value = z.evaluate(variableValues)
    assert value == approx(2)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(3)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(3)

def testPowerWithConstantExponentZero():
    x = Variable("x")
    z = Power(x, Constant(0))
    variableValues = VariableValues({ x: 3 })
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0)
    variableValues = VariableValues({ x: 0 })
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0)
    variableValues = VariableValues({ x: -5 })
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0)

def testPowerWithConstantExponentZeroComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(0))
    variableValues = VariableValues({ x: 1 })
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0)

def testPowerWithConstantExponentZeroDoesntShortCircuit():
    x = Variable("x")
    z = Power(Logarithm(x), Constant(0))
    variableValues = VariableValues({ x: 0 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.allPartialsAt(variableValues)

def testPowerWithConstantExponentNegativeOne():
    x = Variable("x")
    z = Power(x, Constant(-1))
    variableValues = VariableValues({ x: 2 })
    value = z.evaluate(variableValues)
    assert value == approx(0.5)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(-0.25)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-0.25)
    variableValues = VariableValues({ x: 0 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ x: -5 })
    value = z.evaluate(variableValues)
    assert value == approx(-0.2)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(-0.04)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-0.04)

def testPowerWithConstantExponentNegativeOneComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-1))
    variableValues = VariableValues({ x: 1 })
    value = z.evaluate(variableValues)
    assert value == approx(0.5)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(-0.75)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-0.75)

def testPowerWithConstantExponentNegativeTwo():
    x = Variable("x")
    z = Power(x, Constant(-2))
    variableValues = VariableValues({ x: 2 })
    value = z.evaluate(variableValues)
    assert value == approx(0.25)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(-0.25)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-0.25)
    variableValues = VariableValues({ x: 0 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ x: -5 })
    value = z.evaluate(variableValues)
    assert value == approx(0.04)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0.016)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0.016)

def testPowerWithConstantExponentNegativeTwoComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-2))
    variableValues = VariableValues({ x: 1 })
    value = z.evaluate(variableValues)
    assert value == approx(0.25)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(-0.75)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-0.75)

def testPowerWithExponentMadeFromAddingConstants():
    x = Variable("x")
    z = Power(x, Constant(1) + Constant(1))
    variableValues = VariableValues({ x: 3 })
    value = z.evaluate(variableValues)
    assert value == approx(9)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(6)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(6)
    variableValues = VariableValues({ x: 0 })
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0)
    variableValues = VariableValues({ x: -5 })
    value = z.evaluate(variableValues)
    assert value == approx(25)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(-10)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-10)

def testPowerWhereExponentIsAnIntegerRepresentedAsAFloat():
    x = Variable("x")
    z = Power(x, Constant(2.0))
    variableValues = VariableValues({ x: -5 })
    value = z.evaluate(variableValues)
    assert value == approx(25)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(-10)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-10)
