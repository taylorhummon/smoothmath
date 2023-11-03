from __future__ import annotations
from src.forward_accumulation.custom_types import Real

class Result:
    def __init__(
        self: Result,
        value: Real,
        partial: Real
    ) -> None:
        self.value = value
        self.partial = partial

    def toPair(
        self: Result
    ) -> tuple[Real, Real]:
        return (self.value, self.partial)

class InternalResult(Result):
    def __init__(
        self: InternalResult,
        lacksVariables: bool,
        value: Real,
        partial: Real
    ) -> None:
        super().__init__(value, partial)
        self.lacksVariables = lacksVariables

    def toTriple(
        self: InternalResult
    ) -> tuple[bool, Real, Real]:
        return (self.lacksVariables, self.value, self.partial)

    def toResult(
        self: InternalResult
    ) -> Result:
        return Result(self.value, self.partial)
