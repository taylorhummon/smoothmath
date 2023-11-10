from pytest import approx
from src.smooth_expression.variable_values import VariableValues
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.minus import Minus

def testMinus():
    x = Variable("x")
    y = Variable("y")
    z = Minus(x, y)
    variableValues = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variableValues)
    assert value == approx(-1)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(1)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(-1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1)
    assert allPartials.partialWithRespectTo(y) == approx(-1)

def testMinusComposition():
    x = Variable("x")
    y = Variable("y")
    z = Minus(Constant(5) * x, Constant(4) * y)
    variableValues = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variableValues)
    assert value == approx(-2)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(5)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(-4)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(5)
    assert allPartials.partialWithRespectTo(y) == approx(-4)
