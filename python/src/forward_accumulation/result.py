from __future__ import annotations
from src.forward_accumulation.custom_types import numeric

class Result:
    def __init__(
        self: Result,
        value: numeric,
        partial: numeric
    ) -> None:
        self.value = value
        self.partial = partial

    def toPair(
        self: Result
    ) -> tuple[numeric, numeric]:
        return (self.value, self.partial)

class InternalResult(Result):
    def __init__(
        self: InternalResult,
        value: numeric,
        partial: numeric,
        lacksVariables: bool
    ) -> None:
        super().__init__(value, partial)
        self.lacksVariables = lacksVariables

    def toTriple(
        self: InternalResult
    ) -> tuple[numeric, numeric, bool]:
        return (self.value, self.partial, self.lacksVariables)

    def toResult(
        self: InternalResult
    ) -> Result:
        return Result(self.value, self.partial)
