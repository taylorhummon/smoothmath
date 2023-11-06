from pytest import approx, raises
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.multiply import Multiply
from src.smooth_expression.power import Power

def testMultiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    variableValues = { x: 2, y: 3 }
    singleResultForX = z.deriveSingle(variableValues, x)
    assert singleResultForX.value == approx(6)
    assert singleResultForX.partial == approx(3)
    singleResultForY = z.deriveSingle(variableValues, y)
    assert singleResultForY.value == approx(6)
    assert singleResultForY.partial == approx(2)

def testMultiplyComposition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    variableValues = { x: 2, y: 3 }
    singleResultForX = z.deriveSingle(variableValues, x)
    assert singleResultForX.value == approx(20)
    assert singleResultForX.partial == approx(10)
    singleResultForY = z.deriveSingle(variableValues, y)
    assert singleResultForY.value == approx(20)
    assert singleResultForY.partial == approx(10)

def testMultiplyByZero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    singleResult = z.deriveSingle({ x: 2 }, x)
    assert singleResult.value == approx(0)
    assert singleResult.partial == approx(0)

def testMultiplyByZeroDoesntShortCircuit():
    x = Variable("x")
    z = Multiply(Constant(0), Power(Constant(-1), x))
    with raises(DomainException):
        z.deriveSingle({ x: 2 }, x)

def testMultiplyByOne():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    singleResult = z.deriveSingle({ x: 2 }, x)
    assert singleResult.value == approx(2)
    assert singleResult.partial == approx(1)

def testMultiplyMulti():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    multiResult = z.deriveMulti({ x: 2, y: 3 })
    assert multiResult.value == approx(6)
    assert multiResult.partialWithRespectTo(x) == approx(3)
    assert multiResult.partialWithRespectTo(y) == approx(2)

def testMultiplyCompositionMulti():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    multiResult = z.deriveMulti({ x: 2, y: 3 })
    assert multiResult.value == approx(20)
    assert multiResult.partialWithRespectTo(x) == approx(10)
    assert multiResult.partialWithRespectTo(y) == approx(10)

def testMultiplyByZeroMulti():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    multiResult = z.deriveMulti({ x: 2 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(x) == approx(0)

def testMultiplyByZeroDoesntShortCircuitMulti():
    x = Variable("x")
    z = Multiply(Constant(0), Power(Constant(-1), x))
    with raises(DomainException):
        z.deriveMulti({ x: 2 })

def testMultiplyByOneMulti():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    multiResult = z.deriveMulti({ x: 2 })
    assert multiResult.value == approx(2)
    assert multiResult.partialWithRespectTo(x) == approx(1)
