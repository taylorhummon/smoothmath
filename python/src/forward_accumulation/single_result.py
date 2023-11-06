from __future__ import annotations
from src.forward_accumulation.custom_types import Real

class SingleResult:
    def __init__(
        self: SingleResult,
        value: Real,
        partial: Real
    ) -> None:
        self.value = value
        self.partial = partial

    def toPair(
        self: SingleResult
    ) -> tuple[Real, Real]:
        return (self.value, self.partial)

class InternalSingleResult(SingleResult):
    def __init__(
        self: InternalSingleResult,
        lacksVariables: bool,
        value: Real,
        partial: Real
    ) -> None:
        super().__init__(value, partial)
        self.lacksVariables = lacksVariables

    def toTriple(
        self: InternalSingleResult
    ) -> tuple[bool, Real, Real]:
        return (self.lacksVariables, self.value, self.partial)

    def toSingleResult(
        self: InternalSingleResult
    ) -> SingleResult:
        return SingleResult(self.value, self.partial)
