from pytest import approx
import math
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.sine import Sine

def testSine():
    theta = Variable("theta")
    z = Sine(theta)
    variableValues = { theta: 0 }
    assert z.evaluate(variableValues) == approx(0)
    partial = z.partialAt(variableValues, theta)
    assert partial == approx(1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(theta) == approx(1)
    variableValues = { theta: math.pi / 2 }
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, theta)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(theta) == approx(0)

def testSineComposition():
    theta = Variable("theta")
    z = Sine(Constant(2) * theta)
    variableValues = { theta: 0 }
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, theta)
    assert partial == approx(2)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(theta) == approx(2)
