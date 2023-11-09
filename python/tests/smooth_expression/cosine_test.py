from pytest import approx
import math
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.cosine import Cosine

def testCosine():
    theta = Variable("theta")
    z = Cosine(theta)
    variableValues = { theta: 0 }
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, theta)
    assert partial == approx(0)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(theta) == approx(0)
    variableValues = { theta: math.pi / 2 }
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, theta)
    assert partial == approx(-1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(theta) == approx(-1)

def testCosineComposition():
    theta = Variable("theta")
    z = Cosine(Constant(2) * theta)
    variableValues = { theta: math.pi / 4 }
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, theta)
    assert partial == approx(-2)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(theta) == approx(-2)
