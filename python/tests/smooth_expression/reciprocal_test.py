from pytest import approx, raises
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.reciprocal import Reciprocal

def testReciprocal():
    x = Variable("x")
    z = Reciprocal(x)
    variableValues = { x: 2 }
    value = z.evaluate(variableValues)
    assert value == approx(0.5)
    partial = z.partialAt({ x: 2 }, x)
    assert partial == approx(-0.25)
    allPartials = z.allPartialsAt({ x: 2 })
    assert allPartials.partialWithRespectTo(x) == approx(-0.25)
    variableValues = { x: 0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.partialAt(variableValues, x)
    with raises(DomainException):
        z.allPartialsAt(variableValues)
    variableValues = { x: -1 }
    value = z.evaluate(variableValues)
    assert value == approx(-1)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(-1)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-1)

def testReciprocalComposition():
    x = Variable("x")
    z = Reciprocal(Constant(2) * x - Constant(4))
    variableValues = { x: 3 }
    value = z.evaluate(variableValues)
    assert value == approx(0.5)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(-0.5)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-0.5)
