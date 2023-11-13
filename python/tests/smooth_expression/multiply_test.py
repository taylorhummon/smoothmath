from pytest import approx, raises
from src.smooth_expression.custom_exceptions import DomainError
from src.smooth_expression.variable_values import VariableValues
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.multiply import Multiply
from src.smooth_expression.power import Power

def testMultiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    variableValues = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variableValues)
    assert value == approx(6)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(3)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(2)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(3)
    assert allPartials.partialWithRespectTo(y) == approx(2)

def testMultiplyComposition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    variableValues = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variableValues)
    assert value == approx(20)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(10)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(10)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(10)
    assert allPartials.partialWithRespectTo(y) == approx(10)

def testMultiplyByZero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    variableValues = VariableValues({ x: 2 })
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0)

def testMultiplyByZeroDoesntShortCircuit():
    x = Variable("x")
    z = Multiply(Constant(0), Power(Constant(-1), x))
    variableValues = VariableValues({ x: 2 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.allPartialsAt(variableValues)

def testMultiplyByOne():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    variableValues = VariableValues({ x: 2 })
    value = z.evaluate(variableValues)
    assert value == approx(2)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1)
