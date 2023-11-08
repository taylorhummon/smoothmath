from pytest import approx, raises
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.logarithm import Logarithm
from src.smooth_expression.divide import Divide

def testDivide():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    variableValues = { x: 5, y: 2 }
    partialWithRespectToX = z.deriveSingle(variableValues, x)
    assert partialWithRespectToX == approx(0.5)
    partialWithRespectToY = z.deriveSingle(variableValues, y)
    assert partialWithRespectToY == approx(-1.25)
    variableValues = { x: 3, y: 0 }
    with raises(DomainException):
        z.deriveSingle(variableValues, x)
    with raises(DomainException):
        z.deriveSingle(variableValues, y)
    variableValues = { x: 0, y: 0 }
    with raises(DomainException):
        z.deriveSingle(variableValues, x)
    with raises(DomainException):
        z.deriveSingle(variableValues, y)

def testDivideComposition():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    variableValues = { x: 3, y: 1 }
    partialWithRespectToX = z.deriveSingle(variableValues, x)
    assert partialWithRespectToX == approx(0.4)
    partialWithRespectToY = z.deriveSingle(variableValues, y)
    assert partialWithRespectToY == approx(-2)

def testDivideWithConstantNumeratorZero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    partial = z.deriveSingle({ y: 3 }, y)
    assert partial == approx(0)
    partial = z.deriveSingle({ y: 0 }, y)
    assert partial == approx(0)

def testDivideWithConstantNumeratorZeroComposition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    partial = z.deriveSingle({ y: 3 }, y)
    assert partial == approx(0)

def testDivideWithConstantNumeratorZeroDoesntShortCircuit():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    with raises(DomainException):
        z.deriveSingle({ y: 0 }, y)

def testDivideWithConstantDenominatorOne():
    x = Variable("x")
    z = Divide(x, Constant(1))
    partial = z.deriveSingle({ x: 3 }, x)
    assert partial == approx(1)
    partial = z.deriveSingle({ x: 0 }, x)
    assert partial == approx(1)

def testDivideWithConstantDenominatorZero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    with raises(DomainException):
        z.deriveSingle({ x: 3 }, x)
    with raises(DomainException):
        z.deriveSingle({ x: 0 }, x)

def testDivideMulti():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    multiResult = z.deriveMulti({ x: 5, y: 2 })
    assert multiResult.value == approx(2.5)
    assert multiResult.partialWithRespectTo(x) == approx(0.5)
    assert multiResult.partialWithRespectTo(y) == approx(-1.25)
    with raises(DomainException):
        z.deriveMulti({ x: 3, y: 0 })
    with raises(DomainException):
        z.deriveMulti({ x: 0, y: 0 })

def testDivideCompositionMulti():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    multiResult = z.deriveMulti({ x: 3, y: 1 })
    assert multiResult.value == approx(2)
    assert multiResult.partialWithRespectTo(x) == approx(0.4)
    assert multiResult.partialWithRespectTo(y) == approx(-2)

def testDivideWithConstantNumeratorZeroMulti():
    y = Variable("y")
    z = Divide(Constant(0), y)
    multiResult = z.deriveMulti({ y: 3 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(y) == approx(0)
    multiResult = z.deriveMulti({ y: 0 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(y) == approx(0)

def testDivideWithConstantNumeratorZeroCompositionMulti():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    multiResult = z.deriveMulti({ y: 3 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(y) == approx(0)

def testDivideWithConstantNumeratorZeroDoesntShortCircuitMulti():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    with raises(DomainException):
        z.deriveMulti({ y: 0 })

def testDivideWithConstantDenominatorOneMulti():
    x = Variable("x")
    z = Divide(x, Constant(1))
    multiResult = z.deriveMulti({ x: 3 })
    assert multiResult.value == approx(3)
    assert multiResult.partialWithRespectTo(x) == approx(1)
    multiResult = z.deriveMulti({ x: 0 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(x) == approx(1)

def testDivideWithConstantDenominatorZeroMulti():
    x = Variable("x")
    z = Divide(x, Constant(0))
    with raises(DomainException):
        z.deriveMulti({ x: 3 })
    with raises(DomainException):
        z.deriveMulti({ x: 0 })
