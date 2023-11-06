from pytest import approx
import math
from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.exponential import Exponential

def testExponential():
    x = Variable("x")
    z = Exponential(x)
    result = z.derive({ x: 0 }, x)
    assert result.value == approx(1)
    assert result.partial == approx(1)
    result = z.derive({ x: 1 }, x)
    assert result.value == approx(math.e)
    assert result.partial == approx(math.e)
    result = z.derive({ x: -1 }, x)
    assert result.value == approx(1 / math.e)
    assert result.partial == approx(1 / math.e)

def testExponentialComposition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(6))
    result = z.derive({ x: 3 }, x)
    assert result.value == approx(1)
    assert result.partial == approx(2)

def testBaseTwoExponential():
    x = Variable("x")
    z = Exponential(x, 2)
    result = z.derive({ x: 0 }, x)
    assert result.value == approx(1)
    assert result.partial == approx(0.693147180559)
    result = z.derive({ x: 1 }, x)
    assert result.value == approx(2)
    assert result.partial == approx(1.386294361119)
    result = z.derive({ x: -1 }, x)
    assert result.value == approx(0.5)
    assert result.partial == approx(0.346573590279)

def testBaseTwoExponentialComposition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(5), 2)
    result = z.derive({ x: 3 }, x)
    assert result.value == approx(2)
    assert result.partial == approx(2.77258872223)
