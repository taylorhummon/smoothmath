from __future__ import annotations
from typing import TYPE_CHECKING, Mapping
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableOrName
    from src.smooth_expression.variable_values import VariableValues

class VariableValues:
    def __init__(
        self: VariableValues,
        dictionary: Mapping[VariableOrName, Real]
    ) -> None:
        self._dictionary : Mapping[str, Real]
        self._dictionary = {}
        for variableOrName in dictionary:
            name = _nameFrom(variableOrName)
            if name in self._dictionary:
                raise Exception(f"Provided more than one value for variable: {name}")
            self._dictionary[name] = dictionary[variableOrName]

    def valueFor(
        self: VariableValues,
        variableOrName: VariableOrName
    ) -> Real:
        name = _nameFrom(variableOrName)
        value = self._dictionary.get(name, None)
        if value is None:
            raise Exception(f"Missing a value for a variable: {name}")
        return value

def _nameFrom(
    variableOrName: VariableOrName
) -> str:
    return variableOrName if isinstance(variableOrName, str) else variableOrName.name
