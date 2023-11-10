from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.variable_values import VariableValues

def testConstant():
    c = Constant(7)
    variableValues = VariableValues({})
    assert c.evaluate({}) == 7
    x = Variable("x")
    variableValues = VariableValues({ x: 2 })
    partial = c.partialAt(variableValues, x)
    assert partial == 0
    allPartials = c.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == 0
