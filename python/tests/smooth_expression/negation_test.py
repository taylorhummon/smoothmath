from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.negation import Negation

def testNegation():
    x = Variable("x")
    z = Negation(x)
    variableValues = { x: 2 }
    value = z.evaluate(variableValues)
    assert value == -2
    partial = z.partialAt(variableValues, x)
    assert partial == -1
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == -1

def testNegationComposition():
    x = Variable("x")
    z = Negation(Constant(2) * x + Constant(1))
    variableValues = { x: 3 }
    value = z.evaluate(variableValues)
    assert value == -7
    partial = z.partialAt(variableValues, x)
    assert partial == -2
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == -2
