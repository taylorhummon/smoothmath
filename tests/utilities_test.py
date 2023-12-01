from smoothmath.expression import Variable
from smoothmath._private.utilities import is_integer, get_variable_name


def test_is_integer():
    assert is_integer(3) == True
    assert is_integer(3.0) == True
    assert is_integer(3.7) == False


def test_get_variable_names():
    assert get_variable_name(Variable("x")) == "x"
    assert get_variable_name("y") == "y"
