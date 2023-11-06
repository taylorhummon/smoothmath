from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.result import InternalResult
    from src.reverse_accumulation.custom_types import Real, VariableValues
from src.reverse_accumulation.expression import NullaryExpression

class Variable(NullaryExpression):
    def __init__(
        self: Variable,
        name: str
    ) -> None:
        super().__init__(lacksVariables = False)
        if not name:
            raise Exception("Variables must be given a non-blank name")
        self.name: str
        self.name = name
        self._cachedHash: int | None
        self._cachedHash = None

    def _evaluate(
        self: Variable,
        variableValues: VariableValues
    ) -> Real:
        value = variableValues.get(self, None)
        if value is None:
            raise Exception("variableValues is missing a value for a variable")
        return value

    def _derive(
        self: Variable,
        result: InternalResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        result.addSeed(self, seed)

    def __eq__(
        self: Variable,
        other: Any
    ) -> bool:
        return isinstance(other, Variable) and (other.name == self.name)

    def __hash__(self):
        if not self._cachedHash:
            self._cachedHash = hash(self.name)
        return self._cachedHash

    def __str__(
        self: Variable
    ) -> str:
        return self.name
