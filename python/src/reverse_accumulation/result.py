from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Variable

from src.reverse_accumulation.custom_types import numeric

class Result:
    def __init__(
        self: Result
    ):
        self._dict = {}

    def partialWithRespectTo(
        self: Result,
        variable: Variable
    ):
        return self._dict.get(variable, 0)

    def addSeed(
        self: Result,
        variable: Variable,
        seed: numeric
    ):
        self._dict[variable] = seed + self._dict.get(variable, 0)
