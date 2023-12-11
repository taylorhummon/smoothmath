from __future__ import annotations
from typing import Any
import smoothmath as sm
import smoothmath.expression as ex


# This is_integer() function will be no longer needed as of Python 3.12
# when the is_integer() method is defined on int objects.


def is_integer(
    number: sm.real_number
) -> bool:
    return isinstance(number, int) or (isinstance(number, float) and number.is_integer())


def integer_from_integral_real_number(
    number: sm.real_number
) -> int | None:
    if is_integer(number):
        return round(number)
    else:
        return None


def get_class_name(
    any: Any
) -> str:
    return any.__class__.__name__


def get_variable_name(
    variable_or_name: ex.Variable | str
) -> str:
    if isinstance(variable_or_name, str):
        return variable_or_name
    else:
        return variable_or_name.name
