from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number
    from smoothmath.expressions.variable import Variable

# This is_integer() function will be no longer needed as of Python 3.12
# when the is_integer() method is defined on int objects.

def is_integer(
    value: real_number
) -> bool:
    return isinstance(value, int) or value.is_integer()

def get_variable_name(
    variable_or_name: Variable | str
) -> str:
    if isinstance(variable_or_name, str):
        return variable_or_name
    else:
        return variable_or_name.name
