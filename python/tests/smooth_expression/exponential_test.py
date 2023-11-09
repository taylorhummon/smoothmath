from pytest import approx
import math
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.exponential import Exponential

def testExponential():
    x = Variable("x")
    z = Exponential(x)
    variableValues = { x: 0 }
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1)
    variableValues = { x: 1 }
    value = z.evaluate(variableValues)
    assert value == approx(math.e)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(math.e)
    allPartials = z.allPartialsAt(variableValues)
    assert value == approx(math.e)
    assert allPartials.partialWithRespectTo(x) == approx(math.e)
    variableValues = { x: -1 }
    value = z.evaluate(variableValues)
    assert value == approx(1 / math.e)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1 / math.e)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1 / math.e)

def testExponentialComposition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(6))
    variableValues = { x: 3 }
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(2)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(2)

def testBaseTwoExponential():
    x = Variable("x")
    z = Exponential(x, 2)
    variableValues = { x: 0 }
    value = z.evaluate(variableValues)
    assert value == approx(1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0.693147180559)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0.693147180559)
    variableValues = { x: 1 }
    value = z.evaluate(variableValues)
    assert value == approx(2)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1.386294361119)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1.386294361119)
    variableValues = { x: -1 }
    value = z.evaluate(variableValues)
    assert value == approx(0.5)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0.346573590279)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0.346573590279)

def testBaseTwoExponentialComposition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(5), 2)
    variableValues = { x: 3 }
    value = z.evaluate(variableValues)
    assert value == approx(2)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(2.77258872223)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(2.77258872223)
