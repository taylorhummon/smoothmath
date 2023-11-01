from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Variable

from src.reverse_accumulation.custom_types import numeric

class Result:
    def __init__(
        self: Result,
        dictionary: dict[Variable, numeric] | None = None
    ) -> None:
        self._dict : dict[Variable, numeric]
        self._dict = dictionary or {}

    def partialWithRespectTo(
        self: Result,
        variable: Variable
    ) -> numeric:
        return self._dict.get(variable, 0)

class InternalResult(Result):
    def __init__(
        self: InternalResult,
        dictionary: dict[Variable, numeric] | None = None
    ) -> None:
        super().__init__(dictionary)

    def addSeed(
        self: InternalResult,
        variable: Variable,
        seed: numeric
    ) -> None:
        self._dict[variable] = seed + self._dict.get(variable, 0)

    def toResult(
        self: InternalResult
    ) -> Result:
        return Result(self._dict)
