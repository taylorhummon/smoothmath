from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Variable

from src.reverse_accumulation.custom_types import numeric

class ComputedPartials:
    def __init__(
        self: ComputedPartials
    ):
        self._dict = {}

    def partialWithRespectTo(
        self: ComputedPartials,
        variable: Variable
    ):
        return self._dict.get(variable, 0)

    def addSeed(
        self: ComputedPartials,
        variable: Variable,
        seed: numeric
    ):
        self._dict[variable] = seed + self._dict.get(variable, 0)
