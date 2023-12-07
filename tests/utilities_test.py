from smoothmath.expression import Constant, Variable
from smoothmath._private.utilities import is_integer, get_class_name, get_variable_name


def test_is_integer():
    assert is_integer(3) == True
    assert is_integer(3.0) == True
    assert is_integer(3.7) == False


def test_get_class_name():
    assert get_class_name(Variable("x")) == "Variable"
    assert get_class_name(Constant(3)) == "Constant"
    assert get_class_name(3) == "int"


def test_get_variable_name():
    assert get_variable_name(Variable("x")) == "x"
    assert get_variable_name("y") == "y"
