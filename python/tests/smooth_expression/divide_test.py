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
    value = z.evaluate(variableValues)
    assert value == approx(2.5)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(0.5)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(-1.25)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0.5)
    assert allPartials.partialWithRespectTo(y) == approx(-1.25)
    variableValues = { x: 3, y: 0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.partialAt(variableValues, x)
    with raises(DomainException):
        z.partialAt(variableValues, y)
    with raises(DomainException):
        z.allPartialsAt(variableValues)
    variableValues = { x: 0, y: 0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.partialAt(variableValues, x)
    with raises(DomainException):
        z.partialAt(variableValues, y)
    with raises(DomainException):
        z.allPartialsAt(variableValues)

def testDivideComposition():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    variableValues = { x: 3, y: 1 }
    value = z.evaluate(variableValues)
    assert value == approx(2)
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == approx(0.4)
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == approx(-2)
    allPartials = z.allPartialsAt({ x: 3, y: 1 })
    assert allPartials.partialWithRespectTo(x) == approx(0.4)
    assert allPartials.partialWithRespectTo(y) == approx(-2)

def testDivideWithConstantNumeratorZero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    variableValues = { y: 3 }
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt({ y: 3 }, y)
    assert partial == approx(0)
    allPartials = z.allPartialsAt({ y: 3 })
    assert allPartials.partialWithRespectTo(y) == approx(0)
    variableValues = { y: 0 }
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, y)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(y) == approx(0)

def testDivideWithConstantNumeratorZeroComposition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    variableValues = { y: 3 }
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, y)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(y) == approx(0)

def testDivideWithConstantNumeratorZeroDoesntShortCircuit():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    with raises(DomainException):
        z.evaluate({ y: 0 })
    with raises(DomainException):
        z.partialAt({ y: 0 }, y)
    with raises(DomainException):
        z.allPartialsAt({ y: 0 })

def testDivideWithConstantDenominatorOne():
    x = Variable("x")
    z = Divide(x, Constant(1))
    variableValues = { x: 3 }
    value = z.evaluate(variableValues)
    assert value == approx(3)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1)
    variableValues = { x: 0 }
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1)

def testDivideWithConstantDenominatorZero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    variableValues = { x: 3 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.partialAt(variableValues, x)
    with raises(DomainException):
        z.allPartialsAt(variableValues)
    variableValues = { x: 0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.partialAt(variableValues, x)
    with raises(DomainException):
        z.allPartialsAt(variableValues)
