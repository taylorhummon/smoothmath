from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.expression import Variable

class AllPartials:
    def __init__(
        self: AllPartials
    ) -> None:
        self._dictionary : dict[Variable, Real]
        self._dictionary = {}

    def partialWithRespectTo(
        self: AllPartials,
        variable: Variable
    ) -> Real:
        return self._dictionary.get(variable, 0)

    def _addSeed(
        self: AllPartials,
        variable: Variable,
        seed: Real
    ) -> None:
        self._dictionary[variable] = seed + self._dictionary.get(variable, 0)
