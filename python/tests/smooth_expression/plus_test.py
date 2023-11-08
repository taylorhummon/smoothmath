from pytest import approx
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.plus import Plus

def testPlus():
    x = Variable("x")
    y = Variable("y")
    z = Plus(x, y)
    variableValues = { x: 2, y: 3 }
    partialWithRespectToX = z.deriveSingle(variableValues, x)
    assert partialWithRespectToX == approx(1)
    partialWithRespectToY = z.deriveSingle(variableValues, y)
    assert partialWithRespectToY == approx(1)

def testPlusComposition():
    x = Variable("x")
    y = Variable("y")
    z = Plus(Constant(5) * x, Constant(4) * y)
    variableValues = { x: 2, y: 3 }
    partialWithRespectToX = z.deriveSingle(variableValues, x)
    assert partialWithRespectToX == approx(5)
    partialWithRespectToY = z.deriveSingle(variableValues, y)
    assert partialWithRespectToY == approx(4)

def testPlusMulti():
    x = Variable("x")
    y = Variable("y")
    z = Plus(x, y)
    multiResult = z.deriveMulti({ x: 2, y: 3 })
    assert multiResult.value == approx(5)
    assert multiResult.partialWithRespectTo(x) == approx(1)
    assert multiResult.partialWithRespectTo(y) == approx(1)

def testPlusCompositionMulti():
    x = Variable("x")
    y = Variable("y")
    z = Plus(Constant(5) * x, Constant(4) * y)
    multiResult = z.deriveMulti({ x: 2, y: 3 })
    assert multiResult.value == approx(22)
    assert multiResult.partialWithRespectTo(x) == approx(5)
    assert multiResult.partialWithRespectTo(y) == approx(4)
