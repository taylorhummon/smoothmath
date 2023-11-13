from pytest import approx, raises
from src.smooth_expression.custom_exceptions import DomainError
from src.smooth_expression.variable_values import VariableValues
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.square_root import SquareRoot

def testSquareRoot():
    x = Variable("x")
    z = SquareRoot(x)
    variableValues = VariableValues({ x: 4 })
    value = z.evaluate(variableValues)
    assert value == approx(2)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(0.25)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(0.25)
    variableValues = VariableValues({ x: 0 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.allPartialsAt(variableValues)
    variableValues = VariableValues({ x: -1 })
    with raises(DomainError):
        z.evaluate(variableValues)
    with raises(DomainError):
        z.partialAt(variableValues, x)
    with raises(DomainError):
        z.allPartialsAt(variableValues)

def testSquareRootComposition():
    x = Variable("x")
    z = SquareRoot(Constant(2) * x + Constant(7))
    variableValues = VariableValues({ x: 1 })
    value = z.evaluate(variableValues)
    assert value == approx(3)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(1 / 3)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(1 / 3)
