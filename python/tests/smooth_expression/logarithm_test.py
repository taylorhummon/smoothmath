from pytest import approx, raises
import math
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.logarithm import Logarithm

def testLogarithm():
    x = Variable("x")
    z = Logarithm(x)
    singleResult = z.deriveSingle({ x: 1 }, x)
    assert singleResult.value == approx(0)
    assert singleResult.partial == approx(1)
    singleResult = z.deriveSingle({ x: math.e }, x)
    assert singleResult.value == approx(1)
    assert singleResult.partial == approx(1 / math.e)
    with raises(DomainException):
        z.deriveSingle({ x: 0 }, x)
    with raises(DomainException):
        z.deriveSingle({ x: -1 }, x)

def testLogarithmComposition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(3))
    singleResult = z.deriveSingle({ x: 2 }, x)
    assert singleResult.value == approx(0)
    assert singleResult.partial == approx(2)

def testBaseTwoLogarithm():
    x = Variable("x")
    z = Logarithm(x, 2)
    singleResult = z.deriveSingle({ x: 1 }, x)
    assert singleResult.value == approx(0)
    assert singleResult.partial == approx(1.442695040888)
    singleResult = z.deriveSingle({ x: 2 }, x)
    assert singleResult.value == approx(1)
    assert singleResult.partial == approx(0.721347520444)
    with raises(DomainException):
        z.deriveSingle({ x: 0 }, x)
    with raises(DomainException):
        z.deriveSingle({ x: -1 }, x)

def testBaseTwoLogarithmComposition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(6), 2)
    singleResult = z.deriveSingle({ x: 7 }, x)
    assert singleResult.value == approx(3)
    assert singleResult.partial == approx(0.3606737602222)

def testLogarithmMulti():
    x = Variable("x")
    z = Logarithm(x)
    multiResult = z.deriveMulti({ x: 1 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(x) == approx(1)
    multiResult = z.deriveMulti({ x: math.e })
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(x) == approx(1 / math.e)
    with raises(DomainException):
        z.deriveMulti({ x: 0 })
    with raises(DomainException):
        z.deriveMulti({ x: -1 })

def testLogarithmCompositionMulti():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(3))
    multiResult = z.deriveMulti({ x: 2 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(x) == approx(2)

def testBaseTwoLogarithmMulti():
    x = Variable("x")
    z = Logarithm(x, 2)
    multiResult = z.deriveMulti({ x: 1 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(x) == approx(1.442695040888)
    multiResult = z.deriveMulti({ x: 2 })
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(x) == approx(0.721347520444)
    with raises(DomainException):
        z.deriveMulti({ x: 0 })
    with raises(DomainException):
        z.deriveMulti({ x: -1 })

def testBaseTwoLogarithmCompositionMulti():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(6), 2)
    multiResult = z.deriveMulti({ x: 7 })
    assert multiResult.value == approx(3)
    assert multiResult.partialWithRespectTo(x) == approx(0.3606737602222)
