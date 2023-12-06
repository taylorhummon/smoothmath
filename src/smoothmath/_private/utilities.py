from __future__ import annotations
from typing import Any
import smoothmath as sm
import smoothmath.expression as ex


# This is_integer() function will be no longer needed as of Python 3.12
# when the is_integer() method is defined on int objects.


def is_integer(
    value: sm.real_number
) -> bool:
    return isinstance(value, int) or value.is_integer()


def get_class_name(
    any: Any
) -> str:
    return type(any).__name__


def get_variable_name(
    variable_or_name: ex.Variable | str
) -> str:
    if isinstance(variable_or_name, str):
        return variable_or_name
    else:
        return variable_or_name.name
