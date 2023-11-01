from __future__ import annotations
from src.forward_accumulation.custom_types import numeric

# !!! consider hiding depends on from Result exposed to outside world
class Result:
    def __init__(
        self: Result,
        value: numeric,
        partial: numeric,
        lacksVariables: bool
    ):
        self.value = value
        self.partial = partial
        self.lacksVariables = lacksVariables

    def toTriple(
        self: Result
    ) -> tuple[numeric, numeric, bool]:
        return (self.value, self.partial, self.lacksVariables)
