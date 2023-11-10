from pytest import approx
from src.smooth_expression.variable_values import VariableValues
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.plus import Plus

def testPlus():
    x = Variable("x")
    y = Variable("y")
    z = Plus(x, y)
    variableValues = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variableValues)
    assert value == approx(5)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(1)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1)
    assert allPartials.partialWithRespectTo(y) == approx(1)

def testPlusComposition():
    x = Variable("x")
    y = Variable("y")
    z = Plus(Constant(5) * x, Constant(4) * y)
    variableValues = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variableValues)
    assert value == approx(22)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(5)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(4)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(5)
    assert allPartials.partialWithRespectTo(y) == approx(4)
