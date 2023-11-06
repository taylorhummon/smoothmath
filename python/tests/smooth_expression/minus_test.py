from pytest import approx
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.minus import Minus

def testMinus():
    x = Variable("x")
    y = Variable("y")
    z = Minus(x, y)
    variableValues = { x: 2, y: 3 }
    singleResultForX = z.deriveSingle(variableValues, x)
    assert singleResultForX.value == approx(-1)
    assert singleResultForX.partial == approx(1)
    singleResultForY = z.deriveSingle(variableValues, y)
    assert singleResultForY.value == approx(-1)
    assert singleResultForY.partial == approx(-1)

def testMinusComposition():
    x = Variable("x")
    y = Variable("y")
    z = Minus(Constant(5) * x, Constant(4) * y)
    variableValues = { x: 2, y: 3 }
    singleResultForX = z.deriveSingle(variableValues, x)
    assert singleResultForX.value == approx(-2)
    assert singleResultForX.partial == approx(5)
    singleResultForY = z.deriveSingle(variableValues, y)
    assert singleResultForY.value == approx(-2)
    assert singleResultForY.partial == approx(-4)

def testMinusMulti():
    x = Variable("x")
    y = Variable("y")
    z = Minus(x, y)
    multiResult = z.deriveMulti({ x: 2, y: 3 })
    assert multiResult.value == approx(-1)
    assert multiResult.partialWithRespectTo(x) == approx(1)
    assert multiResult.partialWithRespectTo(y) == approx(-1)

def testMinusCompositionMulti():
    x = Variable("x")
    y = Variable("y")
    z = Minus(Constant(5) * x, Constant(4) * y)
    multiResult = z.deriveMulti({ x: 2, y: 3 })
    assert multiResult.value == approx(-2)
    assert multiResult.partialWithRespectTo(x) == approx(5)
    assert multiResult.partialWithRespectTo(y) == approx(-4)
