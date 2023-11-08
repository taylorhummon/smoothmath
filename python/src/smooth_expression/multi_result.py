from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.expression import Variable

class MultiResult:
    def __init__(
        self: MultiResult,
        value: Real,
        dictionary: dict[Variable, Real] | None = None
    ) -> None:
        self.value: Real
        self.value = value # !!! remove value
        self._dict: dict[Variable, Real]
        self._dict = dictionary or {}

    def partialWithRespectTo(
        self: MultiResult,
        variable: Variable
    ) -> Real:
        return self._dict.get(variable, 0)

class InternalMultiResult(MultiResult):
    def __init__(
        self: InternalMultiResult,
        value: Real,
        dictionary: dict[Variable, Real] | None = None
    ) -> None:
        super().__init__(value, dictionary)

    def addSeed(
        self: InternalMultiResult,
        variable: Variable,
        seed: Real
    ) -> None:
        self._dict[variable] = seed + self._dict.get(variable, 0)

    def toMultiResult(
        self: InternalMultiResult
    ) -> MultiResult:
        return MultiResult(self.value, self._dict)
