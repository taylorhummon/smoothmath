from __future__ import annotations
from typing import TYPE_CHECKING, Mapping
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableOrString
    from src.smooth_expression.expression import Variable
from src.smooth_expression.utilities import _nameFromVariableOrName

class AllPartials:
    def __init__(
        self: AllPartials
    ) -> None:
        self._dictionary : Mapping[Variable, Real]
        self._dictionary = {}

    def partialWithRespectTo(
        self: AllPartials,
        variable: VariableOrString
    ) -> Real:
        variableName = _nameFromVariableOrName(variable)
        return self._dictionary.get(variableName, 0)

    def _addSeed(
        self: AllPartials,
        variable: Variable,
        seed: Real
    ) -> None:
        self._dictionary[variable.name] = self._dictionary.get(variable.name, 0) + seed
