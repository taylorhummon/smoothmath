from pytest import approx
import math
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.cosine import Cosine

def testCosine():
    theta = Variable("theta")
    z = Cosine(theta)
    variableValues = { theta: 0 }
    partial = z.deriveSingle(variableValues, theta)
    assert partial == approx(0)
    multiResult = z.deriveMulti(variableValues)
    assert multiResult.value == approx(1)
    assert multiResult.partialWithRespectTo(theta) == approx(0)
    variableValues = { theta: math.pi / 2 }
    partial = z.deriveSingle(variableValues, theta)
    assert partial == approx(-1)
    multiResult = z.deriveMulti(variableValues)
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(theta) == approx(-1)

def testCosineComposition():
    theta = Variable("theta")
    z = Cosine(Constant(2) * theta)
    variableValues = { theta: math.pi / 4 }
    partial = z.deriveSingle(variableValues, theta)
    assert partial == approx(-2)
    multiResult = z.deriveMulti(variableValues)
    assert multiResult.value == approx(0)
    assert multiResult.partialWithRespectTo(theta) == approx(-2)
