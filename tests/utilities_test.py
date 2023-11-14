import smoothmath.utilities as utilities
from smoothmath.expressions.variable import Variable

def test_is_integer():
    assert utilities.is_integer(3) == True
    assert utilities.is_integer(3.0) == True
    assert utilities.is_integer(3.7) == False

def test_get_variable_names():
    assert utilities.get_variable_name(Variable("x")) == "x"
    assert utilities.get_variable_name("y") == "y"
