from pytest import approx, raises
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.logarithm import Logarithm
from src.reverse_accumulation.divide import Divide

def testDivide():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    result = z.derive({ x: 5, y: 2 })
    assert result.value == approx(2.5)
    assert result.partialWithRespectTo(x) == approx(0.5)
    assert result.partialWithRespectTo(y) == approx(-1.25)
    with raises(DomainException):
        z.derive({ x: 3, y: 0 })
    with raises(DomainException):
        z.derive({ x: 0, y: 0 })

def testDivideComposition():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    result = z.derive({ x: 3, y: 1 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(0.4)
    assert result.partialWithRespectTo(y) == approx(-2)

def testDivideWithConstantNumeratorZero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    result = z.derive({ y: 3 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(y) == approx(0)
    result = z.derive({ y: 0 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(y) == approx(0)

def testDivideWithConstantNumeratorZeroComposition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    result = z.derive({ y: 3 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(y) == approx(0)

def testDivideWithConstantNumeratorZeroDoesntShortCircuit():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    with raises(DomainException):
        z.derive({ y: 0 })

def testDivideWithConstantDenominatorOne():
    x = Variable("x")
    z = Divide(x, Constant(1))
    result = z.derive({ x: 3 })
    assert result.value == approx(3)
    assert result.partialWithRespectTo(x) == approx(1)
    result = z.derive({ x: 0 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(1)

def testDivideWithConstantDenominatorZero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    with raises(DomainException):
        z.derive({ x: 3 })
    with raises(DomainException):
        z.derive({ x: 0 })
