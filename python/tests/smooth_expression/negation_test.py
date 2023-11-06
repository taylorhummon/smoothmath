from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.negation import Negation

def testNegation():
    x = Variable("x")
    z = Negation(x)
    variableValues = { x: 2 }
    singleResult = z.deriveSingle(variableValues, x)
    assert singleResult.value == -2
    assert singleResult.partial == -1
    multiResult = z.deriveMulti(variableValues)
    assert multiResult.value == -2
    assert multiResult.partialWithRespectTo(x) == -1

def testNegationComposition():
    x = Variable("x")
    z = Negation(Constant(2) * x + Constant(1))
    variableValues = { x: 3 }
    singleResult = z.deriveSingle(variableValues, x)
    assert singleResult.value == -7
    assert singleResult.partial == -2
    x = Variable("x")
    z = Negation(Constant(2) * x + Constant(1))
    multiResult = z.deriveMulti(variableValues)
    assert multiResult.value == -7
    assert multiResult.partialWithRespectTo(x) == -2
