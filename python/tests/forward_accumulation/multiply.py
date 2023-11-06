from pytest import approx, raises
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.multiply import Multiply
from src.forward_accumulation.power import Power

def testMultiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    variableValues = { x: 2, y: 3 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(6)
    assert resultForX.partial == approx(3)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(6)
    assert resultForY.partial == approx(2)

def testMultiplyComposition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    variableValues = { x: 2, y: 3 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(20)
    assert resultForX.partial == approx(10)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(20)
    assert resultForY.partial == approx(10)

def testMultiplyByZero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    result = z.derive({ x: 2 }, x)
    assert result.value == approx(0)
    assert result.partial == approx(0)

def testMultiplyByZeroDoesntShortCircuit():
    x = Variable("x")
    z = Multiply(Constant(0), Power(Constant(-1), x))
    with raises(DomainException):
        z.derive({ x: 2 }, x)

def testMultiplyByOne():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    result = z.derive({ x: 2 }, x)
    assert result.value == approx(2)
    assert result.partial == approx(1)
