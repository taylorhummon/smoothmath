from __future__ import annotations
from typing import TYPE_CHECKING, Mapping
if TYPE_CHECKING:
    from smoothmath.typing import real_number
    from smoothmath.expressions.variable import Variable

class VariableValues:
    def __init__(
        self: VariableValues,
        dictionary: Mapping[Variable | str, real_number]
    ) -> None:
        self._value_by_variable_name : Mapping[str, real_number]
        self._value_by_variable_name = {}
        for variable_or_name, value in dictionary.items():
            name = utilities.get_variable_name(variable_or_name)
            if name in self._value_by_variable_name:
                raise Exception(f"Provided more than one value for variable: {name}")
            self._value_by_variable_name[name] = value

    def value_for(
        self: VariableValues,
        variable_or_name: Variable | str
    ) -> real_number:
        name = utilities.get_variable_name(variable_or_name)
        value = self._value_by_variable_name.get(name, None)
        if value is None:
            raise Exception(f"Missing a value for a variable: {name}")
        return value

# imports needed for class implementation
import smoothmath.utilities as utilities
