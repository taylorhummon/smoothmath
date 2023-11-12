from __future__ import annotations
from typing import TYPE_CHECKING, Mapping
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableOrString
    from src.smooth_expression.variable_values import VariableValues
from src.smooth_expression.utilities import _nameFromVariableOrName

class VariableValues:
    def __init__(
        self: VariableValues,
        dictionary: Mapping[VariableOrString, Real]
    ) -> None:
        self._dictionary : Mapping[str, Real]
        self._dictionary = {}
        for variableOrName, value in dictionary.items():
            name = _nameFromVariableOrName(variableOrName)
            if name in self._dictionary:
                raise Exception(f"Provided more than one value for variable: {name}")
            self._dictionary[name] = value

    def valueFor(
        self: VariableValues,
        variableOrName: VariableOrString
    ) -> Real:
        name = _nameFromVariableOrName(variableOrName)
        value = self._dictionary.get(name, None)
        if value is None:
            raise Exception(f"Missing a value for a variable: {name}")
        return value
