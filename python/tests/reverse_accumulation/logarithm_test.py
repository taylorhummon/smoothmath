from pytest import approx, raises
import math
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.logarithm import Logarithm

def testLogarithm():
    x = Variable("x")
    z = Logarithm(x)
    result = z.derive({ x: 1 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(1)
    result = z.derive({ x: math.e })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(1 / math.e)
    with raises(DomainException):
        z.derive({ x: 0 })
    with raises(DomainException):
        z.derive({ x: -1 })

def testLogarithmComposition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(3))
    result = z.derive({ x: 2 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(2)

def testBaseTwoLogarithm():
    x = Variable("x")
    z = Logarithm(x, 2)
    result = z.derive({ x: 1 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(1.442695040888)
    result = z.derive({ x: 2 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(0.721347520444)
    with raises(DomainException):
        z.derive({ x: 0 })
    with raises(DomainException):
        z.derive({ x: -1 })

def testBaseTwoLogarithmComposition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(6), 2)
    result = z.derive({ x: 7 })
    assert result.value == approx(3)
    assert result.partialWithRespectTo(x) == approx(0.3606737602222)
