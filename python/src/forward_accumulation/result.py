from __future__ import annotations
from src.forward_accumulation.custom_types import numeric
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Variable

class Result:
    def __init__(
        self: Result,
        value: numeric,
        partial: numeric,
        dependsOn: set[Variable]
    ):
        self.value = value
        self.partial = partial
        self.dependsOn = dependsOn

    def toTriple(
        self: Result
    ) -> tuple[numeric, numeric, set[Variable]]:
        return (self.value, self.partial, self.dependsOn)
