from pytest import approx, raises
import math
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.logarithm import Logarithm

def testLogarithm():
    x = Variable("x")
    z = Logarithm(x)
    variableValues = { x: 1 }
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1)
    variableValues = { x: math.e }
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1 / math.e)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1 / math.e)
    variableValues = { x: 0 }
    with raises(DomainException):
        z.evaluate({ x: 0 })
    with raises(DomainException):
        z.partialAt({ x: 0 }, x)
    with raises(DomainException):
        z.allPartialsAt({ x: 0 })
    variableValues = { x: -1 }
    with raises(DomainException):
        z.evaluate({ x: -1 })
    with raises(DomainException):
        z.partialAt({ x: -1 }, x)
    with raises(DomainException):
        z.allPartialsAt({ x: -1 })

def testLogarithmComposition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(3))
    variableValues = { x: 2 }
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(2)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(2)

def testBaseTwoLogarithm():
    x = Variable("x")
    z = Logarithm(x, 2)
    variableValues = { x: 1 }
    value = z.evaluate(variableValues)
    assert value == approx(0)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1.442695040888)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1.442695040888)
    variableValues = { x: 2 }
    value = z.evaluate(variableValues)
    assert value == approx(1)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0.721347520444)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0.721347520444)

    with raises(DomainException):
        z.evaluate({ x: 0 })
    with raises(DomainException):
        z.partialAt({ x: 0 }, x)
    with raises(DomainException):
        z.allPartialsAt({ x: 0 })

    with raises(DomainException):
        z.evaluate({ x: -1 })
    with raises(DomainException):
        z.partialAt({ x: -1 }, x)
    with raises(DomainException):
        z.allPartialsAt({ x: -1 })

def testBaseTwoLogarithmComposition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(6), 2)
    variableValues = { x: 7 }
    value = z.evaluate(variableValues)
    assert value == approx(3)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0.3606737602222)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0.3606737602222)
