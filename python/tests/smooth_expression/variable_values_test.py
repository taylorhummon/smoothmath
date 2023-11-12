from pytest import raises
from src.smooth_expression.variable import Variable
from src.smooth_expression.variable_values import VariableValues

def testVariableValues():
    x = Variable("x")
    y = Variable("y")
    variableValues = VariableValues({ x: 3, y: 4 })
    assert variableValues.valueFor(x) == 3
    assert variableValues.valueFor(y) == 4
    assert variableValues.valueFor("x") == 3
    assert variableValues.valueFor("y") == 4
    variableValues = VariableValues({ "x": 5, "y": 6 })
    assert variableValues.valueFor(x) == 5
    assert variableValues.valueFor(y) == 6
    assert variableValues.valueFor("x") == 5
    assert variableValues.valueFor("y") == 6

def testVariableValuesWhenMissingAVariable():
    x = Variable("x")
    y = Variable("y")
    variableValues = VariableValues({ x: 3 })
    with raises(Exception):
        variableValues.valueFor(y)

def testVariableValuesWhenProvidingTheSameVariableTwice():
    x = Variable("x")
    y = Variable("y")
    with raises(Exception):
        VariableValues({ x: 3, y: 4, "x": 5 })
