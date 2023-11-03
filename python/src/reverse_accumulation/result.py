from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Variable

from src.reverse_accumulation.custom_types import Real

class Result:
    def __init__(
        self: Result,
        value: Real,
        dictionary: dict[Variable, Real] | None = None
    ) -> None:
        self.value : Real
        self.value = value
        self._dict : dict[Variable, Real]
        self._dict = dictionary or {}

    def partialWithRespectTo(
        self: Result,
        variable: Variable
    ) -> Real:
        return self._dict.get(variable, 0)

class InternalResult(Result):
    def __init__(
        self: InternalResult,
        value: Real,
        dictionary: dict[Variable, Real] | None = None
    ) -> None:
        super().__init__(value, dictionary)

    def addSeed(
        self: InternalResult,
        variable: Variable,
        seed: Real
    ) -> None:
        self._dict[variable] = seed + self._dict.get(variable, 0)

    def toResult(
        self: InternalResult
    ) -> Result:
        return Result(self.value, self._dict)
