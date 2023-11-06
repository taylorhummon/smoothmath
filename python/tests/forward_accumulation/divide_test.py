from pytest import approx, raises
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.logarithm import Logarithm
from src.forward_accumulation.divide import Divide

def testDivide():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    variableValues = { x: 5, y: 2 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(2.5)
    assert resultForX.partial == approx(0.5)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(2.5)
    assert resultForY.partial == approx(-1.25)
    variableValues = { x: 3, y: 0 }
    with raises(DomainException):
        z.derive(variableValues, x)
    with raises(DomainException):
        z.derive(variableValues, y)
    variableValues = { x: 0, y: 0 }
    with raises(DomainException):
        z.derive(variableValues, x)
    with raises(DomainException):
        z.derive(variableValues, y)

def testDivideComposition():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    variableValues = { x: 3, y: 1 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(2)
    assert resultForX.partial == approx(0.4)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(2)
    assert resultForY.partial == approx(-2)

def testDivideWithConstantNumeratorZero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    result = z.derive({ y: 3 }, y)
    assert result.value == approx(0)
    assert result.partial == approx(0)
    result = z.derive({ y: 0 }, y)
    assert result.value == approx(0)
    assert result.partial == approx(0)

def testDivideWithConstantNumeratorZeroComposition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    result = z.derive({ y: 3 }, y)
    assert result.value == approx(0)
    assert result.partial == approx(0)

def testDivideWithConstantNumeratorZeroDoesntShortCircuit():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    with raises(DomainException):
        z.derive({ y: 0 }, y)

def testDivideWithConstantDenominatorOne():
    x = Variable("x")
    z = Divide(x, Constant(1))
    result = z.derive({ x: 3 }, x)
    assert result.value == approx(3)
    assert result.partial == approx(1)
    result = z.derive({ x: 0 }, x)
    assert result.value == approx(0)
    assert result.partial == approx(1)

def testDivideWithConstantDenominatorZero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    with raises(DomainException):
        z.derive({ x: 3 }, x)
    with raises(DomainException):
        z.derive({ x: 0 }, x)
