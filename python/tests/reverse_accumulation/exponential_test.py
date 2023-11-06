from pytest import approx
import math
from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.exponential import Exponential

def testExponential():
    x = Variable("x")
    z = Exponential(x)
    result = z.derive({ x: 0 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(1)
    result = z.derive({ x: 1 })
    assert result.value == approx(math.e)
    assert result.partialWithRespectTo(x) == approx(math.e)
    result = z.derive({ x: -1 })
    assert result.value == approx(1 / math.e)
    assert result.partialWithRespectTo(x) == approx(1 / math.e)

def testExponentialComposition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(6))
    result = z.derive({ x: 3 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(2)

def testBaseTwoExponential():
    x = Variable("x")
    z = Exponential(x, 2)
    result = z.derive({ x: 0 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(0.693147180559)
    result = z.derive({ x: 1 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(1.386294361119)
    result = z.derive({ x: -1 })
    assert result.value == approx(0.5)
    assert result.partialWithRespectTo(x) == approx(0.346573590279)

def testBaseTwoExponentialComposition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(5), 2)
    result = z.derive({ x: 3 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(2.77258872223)
