from pytest import approx, raises
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.multiply import Multiply
from src.reverse_accumulation.power import Power

def testMultiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(6)
    assert result.partialWithRespectTo(x) == approx(3)
    assert result.partialWithRespectTo(y) == approx(2)

def testMultiplyComposition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(20)
    assert result.partialWithRespectTo(x) == approx(10)
    assert result.partialWithRespectTo(y) == approx(10)

def testMultiplyByZero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    result = z.derive({ x: 2 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(0)

def testMultiplyByZeroDoesntShortCircuit():
    x = Variable("x")
    z = Multiply(Constant(0), Power(Constant(-1), x))
    with raises(DomainException):
        z.derive({ x: 2 })

def testMultiplyByOne():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    result = z.derive({ x: 2 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(1)
