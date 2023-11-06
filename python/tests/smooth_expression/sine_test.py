from pytest import approx
import math
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.sine import Sine

def testSine():
    theta = Variable("theta")
    z = Sine(theta)
    singleResult = z.deriveSingle({ theta: 0 }, theta)
    assert singleResult.value == approx(0)
    assert singleResult.partial == approx(1)
    singleResult = z.deriveSingle({ theta: math.pi / 2 }, theta)
    assert singleResult.value == approx(1)
    assert singleResult.partial == approx(0)

def testSineComposition():
    theta = Variable("theta")
    z = Sine(Constant(2) * theta)
    singleResult = z.deriveSingle({ theta: 0 }, theta)
    assert singleResult.value == approx(0)
    assert singleResult.partial == approx(2)

def testSineMulti():
    theta = Variable("theta")
    z = Sine(theta)
    multiResult = z.deriveMulti({ theta: 0 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(theta) == approx(1)
    multiResult = z.deriveMulti({ theta: math.pi / 2 })
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(theta) == approx(0)

def testSineCompositionMulti():
    theta = Variable("theta")
    z = Sine(Constant(2) * theta)
    multiResult = z.deriveMulti({ theta: 0 })
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(theta) == approx(2)
