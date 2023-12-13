import math
from smoothmath.expression import Constant, Variable
from smoothmath._private.utilities import (
    is_integer,
    integer_from_integral_real_number,
    get_class_name,
    get_variable_name
)


def test_is_integer():
    assert is_integer(3) == True
    assert is_integer(3.0) == True
    assert is_integer(3.7) == False
    assert is_integer("3") == False # type: ignore
    assert is_integer(0.0) == True
    assert is_integer(-0.0) == True
    assert is_integer(math.inf) == False
    assert is_integer(-math.inf) == False
    assert is_integer(math.nan) == False


def test_integer_from_integral_real_number():
    assert integer_from_integral_real_number(3) == 3
    assert integer_from_integral_real_number(3.0) == 3
    assert integer_from_integral_real_number(3.7) == None
    assert integer_from_integral_real_number("3") == None # type: ignore
    assert integer_from_integral_real_number(0.0) == 0
    assert integer_from_integral_real_number(-0.0) == 0
    assert integer_from_integral_real_number(math.inf) == None
    assert integer_from_integral_real_number(-math.inf) == None
    assert integer_from_integral_real_number(math.nan) == None


def test_get_class_name():
    assert get_class_name(Variable("x")) == "Variable"
    assert get_class_name(Constant(3)) == "Constant"
    assert get_class_name(3) == "int"


def test_get_variable_name():
    assert get_variable_name(Variable("x")) == "x"
    assert get_variable_name("y") == "y"
