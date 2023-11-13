from pytest import raises
from smoothmath.expressions.variable import Variable
from smoothmath.variable_values import VariableValues

def testVariableValues():
    x = Variable("x")
    y = Variable("y")
    variable_values = VariableValues({ x: 3, y: 4 })
    assert variable_values.value_for(x) == 3
    assert variable_values.value_for(y) == 4
    assert variable_values.value_for("x") == 3
    assert variable_values.value_for("y") == 4
    variable_values = VariableValues({ "x": 5, "y": 6 })
    assert variable_values.value_for(x) == 5
    assert variable_values.value_for(y) == 6
    assert variable_values.value_for("x") == 5
    assert variable_values.value_for("y") == 6

def testVariableValuesWhenMissingAVariable():
    x = Variable("x")
    y = Variable("y")
    variable_values = VariableValues({ x: 3 })
    with raises(Exception):
        variable_values.value_for(y)

def testVariableValuesWhenProvidingTheSameVariableTwice():
    x = Variable("x")
    y = Variable("y")
    with raises(Exception):
        VariableValues({ x: 3, y: 4, "x": 5 })
