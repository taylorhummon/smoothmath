from pytest import approx, raises
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.square_root import SquareRoot

def testSquareRoot():
    x = Variable("x")
    z = SquareRoot(x)
    variableValues = { x: 4 }
    value = z.evaluate(variableValues)
    assert value == approx(2)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0.25)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0.25)
    variableValues = { x: 0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.partialAt(variableValues, x)
    with raises(DomainException):
        z.allPartialsAt(variableValues)
    variableValues = { x: -1 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.partialAt(variableValues, x)
    with raises(DomainException):
        z.allPartialsAt(variableValues)

def testSquareRootComposition():
    x = Variable("x")
    z = SquareRoot(Constant(2) * x + Constant(7))
    variableValues = { x: 1 }
    value = z.evaluate(variableValues)
    assert value == approx(3)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1 / 3)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1 / 3)
