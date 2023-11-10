from src.smooth_expression.variable import Variable
from src.smooth_expression.variable_values import VariableValues

def testVariable():
    x = Variable("x")
    variableValues = VariableValues({ x: 2 })
    value = x.evaluate(variableValues)
    assert value == 2
    partial = x.partialAt(variableValues, x)
    assert partial == 1
    y = Variable("y")
    variableValues = VariableValues({ x: 2, y: 3 })
    allPartials = x.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == 1
    assert allPartials.partialWithRespectTo(y) == 0
