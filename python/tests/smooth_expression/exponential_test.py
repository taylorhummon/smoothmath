from pytest import approx
import math
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.exponential import Exponential

def testExponential():
    x = Variable("x")
    z = Exponential(x)
    partial = z.deriveSingle({ x: 0 }, x)
    assert partial == approx(1)
    partial = z.deriveSingle({ x: 1 }, x)
    assert partial == approx(math.e)
    partial = z.deriveSingle({ x: -1 }, x)
    assert partial == approx(1 / math.e)

def testExponentialComposition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(6))
    partial = z.deriveSingle({ x: 3 }, x)
    assert partial == approx(2)

def testBaseTwoExponential():
    x = Variable("x")
    z = Exponential(x, 2)
    partial = z.deriveSingle({ x: 0 }, x)
    assert partial == approx(0.693147180559)
    partial = z.deriveSingle({ x: 1 }, x)
    assert partial == approx(1.386294361119)
    partial = z.deriveSingle({ x: -1 }, x)
    assert partial == approx(0.346573590279)

def testBaseTwoExponentialComposition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(5), 2)
    partial = z.deriveSingle({ x: 3 }, x)
    assert partial == approx(2.77258872223)

def testExponentialMulti():
    x = Variable("x")
    z = Exponential(x)
    result = z.deriveMulti({ x: 0 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(1)
    result = z.deriveMulti({ x: 1 })
    assert result.value == approx(math.e)
    assert result.partialWithRespectTo(x) == approx(math.e)
    result = z.deriveMulti({ x: -1 })
    assert result.value == approx(1 / math.e)
    assert result.partialWithRespectTo(x) == approx(1 / math.e)

def testExponentialCompositionMulti():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(6))
    result = z.deriveMulti({ x: 3 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(2)

def testBaseTwoExponentialMulti():
    x = Variable("x")
    z = Exponential(x, 2)
    result = z.deriveMulti({ x: 0 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(0.693147180559)
    result = z.deriveMulti({ x: 1 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(1.386294361119)
    result = z.deriveMulti({ x: -1 })
    assert result.value == approx(0.5)
    assert result.partialWithRespectTo(x) == approx(0.346573590279)

def testBaseTwoExponentialCompositionMulti():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(5), 2)
    result = z.deriveMulti({ x: 3 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(2.77258872223)
